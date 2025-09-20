#!/usr/bin/env python3
"""
Prompt Flow Reader - Read multiple prompt/instruction files in order

This module provides utilities to read and process prompt and instruction files
from the GitHub Copilot Playbook repository in a structured manner.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class FileType(Enum):
    """Enumeration for different file types"""
    PROMPT = "prompt"
    INSTRUCTION = "instruction"
    DOCUMENT = "document"

@dataclass
class FileMetadata:
    """Metadata extracted from file frontmatter"""
    file_type: FileType
    apply_to: Optional[str] = None
    mode: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    raw_frontmatter: Optional[Dict] = None

@dataclass
class ProcessedFile:
    """Container for a processed file with metadata and content"""
    file_path: Path
    metadata: FileMetadata
    content: str
    frontmatter: Optional[Dict] = None

class PromptFlowReader:
    """
    Main class for reading and processing prompt/instruction files
    """
    
    def __init__(self, base_path: str = None):
        """
        Initialize the PromptFlowReader
        
        Args:
            base_path: Base directory path. If None, uses current working directory.
        """
        if base_path is None:
            self.base_path = Path.cwd()
        else:
            self.base_path = Path(base_path)
        
        # Define common file patterns
        self.instruction_patterns = [
            ".github/instructions/**/*.instructions.md",
            "instructions/**/*.instructions.md",
            "**/*.instructions.md"
        ]
        
        self.prompt_patterns = [
            ".github/prompts/**/*.prompt.md", 
            "prompts/**/*.prompt.md",
            "**/*.prompt.md"
        ]
        
        self.doc_patterns = [
            "docs/**/*.md",
            "*.md"
        ]
    
    def _extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """
        Extract YAML frontmatter from markdown content
        
        Args:
            content: Raw file content
            
        Returns:
            Tuple of (frontmatter_dict, content_without_frontmatter)
        """
        lines = content.split('\n')
        
        # Check if file starts with frontmatter delimiter
        if not lines or lines[0].strip() != '---':
            return None, content
        
        # Find end of frontmatter
        end_idx = None
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                end_idx = i
                break
        
        if end_idx is None:
            return None, content
        
        try:
            # Parse YAML frontmatter
            frontmatter_text = '\n'.join(lines[1:end_idx])
            frontmatter = yaml.safe_load(frontmatter_text) if frontmatter_text.strip() else {}
            
            # Return content without frontmatter
            remaining_content = '\n'.join(lines[end_idx + 1:])
            return frontmatter, remaining_content
            
        except yaml.YAMLError:
            return None, content
    
    def _determine_file_type(self, file_path: Path, frontmatter: Optional[Dict]) -> FileType:
        """
        Determine the file type based on path and frontmatter
        
        Args:
            file_path: Path to the file
            frontmatter: Parsed frontmatter dictionary
            
        Returns:
            FileType enum value
        """
        file_name = file_path.name.lower()
        
        if '.instructions.md' in file_name:
            return FileType.INSTRUCTION
        elif '.prompt.md' in file_name:
            return FileType.PROMPT
        elif frontmatter:
            if 'applyTo' in frontmatter or 'applyto' in frontmatter:
                return FileType.INSTRUCTION
            elif 'mode' in frontmatter or 'model' in frontmatter:
                return FileType.PROMPT
        
        return FileType.DOCUMENT
    
    def _create_metadata(self, file_path: Path, frontmatter: Optional[Dict]) -> FileMetadata:
        """
        Create FileMetadata from frontmatter
        
        Args:
            file_path: Path to the file
            frontmatter: Parsed frontmatter dictionary
            
        Returns:
            FileMetadata object
        """
        file_type = self._determine_file_type(file_path, frontmatter)
        
        if not frontmatter:
            return FileMetadata(file_type=file_type)
        
        return FileMetadata(
            file_type=file_type,
            apply_to=frontmatter.get('applyTo') or frontmatter.get('applyto'),
            mode=frontmatter.get('mode'),
            model=frontmatter.get('model'),
            description=frontmatter.get('description'),
            raw_frontmatter=frontmatter
        )
    
    def read_file(self, file_path: Path) -> ProcessedFile:
        """
        Read and process a single file
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            ProcessedFile object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file can't be read
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except IOError as e:
            raise IOError(f"Failed to read file {file_path}: {e}")
        
        frontmatter, clean_content = self._extract_frontmatter(content)
        metadata = self._create_metadata(file_path, frontmatter)
        
        return ProcessedFile(
            file_path=file_path,
            metadata=metadata,
            content=clean_content,
            frontmatter=frontmatter
        )
    
    def find_files_by_pattern(self, patterns: List[str]) -> List[Path]:
        """
        Find files matching the given glob patterns
        
        Args:
            patterns: List of glob patterns to search for
            
        Returns:
            List of Path objects for matching files
        """
        found_files = []
        
        for pattern in patterns:
            found_files.extend(self.base_path.glob(pattern))
        
        # Remove duplicates and sort
        unique_files = sorted(set(found_files))
        return [f for f in unique_files if f.is_file()]
    
    def read_instruction_files(self) -> List[ProcessedFile]:
        """
        Read all instruction files in the repository
        
        Returns:
            List of ProcessedFile objects for instruction files
        """
        instruction_files = self.find_files_by_pattern(self.instruction_patterns)
        return [self.read_file(f) for f in instruction_files]
    
    def read_prompt_files(self) -> List[ProcessedFile]:
        """
        Read all prompt files in the repository
        
        Returns:
            List of ProcessedFile objects for prompt files
        """
        prompt_files = self.find_files_by_pattern(self.prompt_patterns)
        return [self.read_file(f) for f in prompt_files]
    
    def read_all_files(self) -> Dict[str, List[ProcessedFile]]:
        """
        Read all prompt, instruction, and document files
        
        Returns:
            Dictionary with keys 'instructions', 'prompts', 'documents'
            and corresponding lists of ProcessedFile objects
        """
        instructions = self.read_instruction_files()
        prompts = self.read_prompt_files()
        
        # Find additional document files
        doc_files = self.find_files_by_pattern(self.doc_patterns)
        
        # Filter out files already processed as instructions/prompts
        processed_paths = {f.file_path for f in instructions + prompts}
        remaining_docs = [f for f in doc_files if f not in processed_paths]
        documents = [self.read_file(f) for f in remaining_docs]
        
        return {
            'instructions': instructions,
            'prompts': prompts,
            'documents': documents
        }
    
    def read_files_in_order(self, file_paths: List[str]) -> List[ProcessedFile]:
        """
        Read specific files in the given order
        
        Args:
            file_paths: List of file paths to read in order
            
        Returns:
            List of ProcessedFile objects in the specified order
        """
        processed_files = []
        
        for file_path_str in file_paths:
            file_path = self.base_path / file_path_str
            try:
                processed_file = self.read_file(file_path)
                processed_files.append(processed_file)
            except (FileNotFoundError, IOError) as e:
                print(f"Warning: Could not read {file_path}: {e}")
        
        return processed_files
    
    def print_file_summary(self, processed_file: ProcessedFile) -> None:
        """
        Print a summary of a processed file
        
        Args:
            processed_file: ProcessedFile to summarize
        """
        print(f"\n📄 {processed_file.file_path.name}")
        print(f"   Path: {processed_file.file_path}")
        print(f"   Type: {processed_file.metadata.file_type.value}")
        
        if processed_file.metadata.apply_to:
            print(f"   Applies to: {processed_file.metadata.apply_to}")
        if processed_file.metadata.mode:
            print(f"   Mode: {processed_file.metadata.mode}")
        if processed_file.metadata.model:
            print(f"   Model: {processed_file.metadata.model}")
        if processed_file.metadata.description:
            print(f"   Description: {processed_file.metadata.description}")
        
        content_length = len(processed_file.content)
        print(f"   Content length: {content_length} characters")
        
        # Show first few lines of content
        lines = processed_file.content.strip().split('\n')[:3]
        if lines and lines[0]:
            print(f"   Preview: {lines[0][:80]}{'...' if len(lines[0]) > 80 else ''}")
    
    def append_and_print_prompt_context(self, prompt_files: List[ProcessedFile]) -> str:
        """
        Append the context of all prompt files and print the combined content
        
        Args:
            prompt_files: List of ProcessedFile objects for prompt files
            
        Returns:
            Combined context string of all prompt files
        """
        if not prompt_files:
            print("\n🚫 No prompt files found to append.")
            return ""
        
        print("\n" + "=" * 70)
        print("🔗 COMBINED PROMPT CONTEXT")
        print("=" * 70)
        
        combined_context = []
        
        for i, prompt_file in enumerate(prompt_files, 1):
            print(f"\n📋 Prompt {i}: {prompt_file.file_path.name}")
            print("-" * 50)
            
            # Add file header to context
            header = f"# Prompt {i}: {prompt_file.file_path.name}\n"
            header += f"# Path: {prompt_file.file_path}\n"
            
            if prompt_file.metadata.description:
                header += f"# Description: {prompt_file.metadata.description}\n"
            if prompt_file.metadata.mode:
                header += f"# Mode: {prompt_file.metadata.mode}\n"
            if prompt_file.metadata.model:
                header += f"# Model: {prompt_file.metadata.model}\n"
            
            header += "\n"
            
            combined_context.append(header)
            combined_context.append(prompt_file.content)
            combined_context.append("\n" + "─" * 50 + "\n")
            
            # Print the content
            print(f"📄 Content ({len(prompt_file.content)} characters):")
            print(prompt_file.content)
            print("─" * 50)
        
        # Join all contexts
        final_context = "\n".join(combined_context)
        
        print(f"\n✅ Combined {len(prompt_files)} prompt files")
        print(f"📊 Total combined length: {len(final_context)} characters")
        
        # Print the final combined context
        print("\n" + "=" * 70)
        print("📝 FINAL COMBINED PROMPT CONTEXT")
        print("=" * 70)
        print(final_context)
        
        return final_context


def main():
    """
    Example usage of the PromptFlowReader
    """
    # Initialize reader with current directory
    reader = PromptFlowReader()
    
    print("🚀 GitHub Copilot Playbook - Prompt Flow Reader")
    print("=" * 50)
    
    # Read all files by category
    all_files = reader.read_all_files()
    
    # Display summary
    for category, files in all_files.items():
        print(f"\n📁 {category.upper()} ({len(files)} files)")
        print("-" * 30)
        
        for processed_file in files:
            reader.print_file_summary(processed_file)
    
    print(f"\n✅ Total files processed: {sum(len(files) for files in all_files.values())}")
    
    # Example: Read specific files in order
    print("\n🔄 Reading specific files in order:")
    print("-" * 40)
    
    specific_files = [
        ".github/instructions/generate_unit_test.instructions.md",
        ".github/instructions/summarize_logic.instructions.md", 
        ".github/prompts/summarize_logic.prompt.md"
    ]
    
    ordered_files = reader.read_files_in_order(specific_files)
    
    for i, processed_file in enumerate(ordered_files, 1):
        print(f"\n{i}. {processed_file.file_path.name}")
        print(f"   Type: {processed_file.metadata.file_type.value}")
        if processed_file.metadata.description:
            print(f"   Description: {processed_file.metadata.description}")
    
    # NEW: Append and print prompt context
    prompt_files = all_files.get('prompts', [])
    if prompt_files:
        combined_prompt_context = reader.append_and_print_prompt_context(prompt_files)
        
        # Optionally save the combined context to a file
        output_file = reader.base_path / "combined_prompt_context.md"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(combined_prompt_context)
            print(f"\n💾 Combined prompt context saved to: {output_file}")
        except IOError as e:
            print(f"\n❌ Failed to save combined context: {e}")
    else:
        print("\n🚫 No prompt files found to combine.")


if __name__ == "__main__":
    main()