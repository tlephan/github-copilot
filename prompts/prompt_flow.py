#!/usr/bin/env python3
"""
Prompt Flow Reader - Read multiple prompt/instruction files in order

This module provides utilities to read and process prompt and instruction files
from the GitHub Copilot Playbook repository in a structured manner.
"""

import os
import yaml
import argparse
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

@dataclass
class FlowConfig:
    """Configuration loaded from YAML flow file"""
    name: str
    version: str = "1.0.0"
    description: str = ""
    config: Dict = None
    flow: List[Dict] = None
    file_patterns: Dict = None
    output: Dict = None
    execution: Dict = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}
        if self.flow is None:
            self.flow = []
        if self.file_patterns is None:
            self.file_patterns = {"include": [], "exclude": []}
        if self.output is None:
            self.output = {"format": "combined"}
        if self.execution is None:
            self.execution = {"model": "Claude Sonnet 4 (copilot)", "mode": "agent"}

class PromptFlowReader:
    """
    Main class for reading and processing prompt/instruction files
    """
    
    def __init__(self, base_path: str = None, config: FlowConfig = None):
        """
        Initialize the PromptFlowReader
        
        Args:
            base_path: Base directory path. If None, uses current working directory.
            config: FlowConfig object with execution parameters
        """
        if base_path is None:
            self.base_path = Path.cwd()
        else:
            self.base_path = Path(base_path)
        
        self.config = config
        
        # Define common file patterns (can be overridden by config)
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
        
        # Override patterns if config is provided
        if self.config and self.config.file_patterns:
            if "include" in self.config.file_patterns:
                # Use config patterns for discovery
                self.config_patterns = self.config.file_patterns["include"]
            if "exclude" in self.config.file_patterns:
                self.exclude_patterns = self.config.file_patterns["exclude"]
        else:
            self.config_patterns = []
            self.exclude_patterns = []
    
    @classmethod
    def load_config(cls, config_file: Path) -> FlowConfig:
        """
        Load configuration from YAML file
        
        Args:
            config_file: Path to the YAML configuration file
            
        Returns:
            FlowConfig object
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file has invalid YAML
        """
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            return FlowConfig(
                name=config_data.get('name', 'unnamed_flow'),
                version=config_data.get('version', '1.0.0'),
                description=config_data.get('description', ''),
                config=config_data.get('config', {}),
                flow=config_data.get('flow', []),
                file_patterns=config_data.get('file_patterns', {}),
                output=config_data.get('output', {}),
                execution=config_data.get('execution', {})
            )
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in config file {config_file}: {e}")
    
    def execute_flow(self) -> Dict[str, any]:
        """
        Execute the configured flow steps in order
        
        Returns:
            Dictionary containing execution results
        """
        if not self.config or not self.config.flow:
            print("⚠️  No flow configuration found. Running default behavior.")
            return self._execute_default_flow()
        
        print(f"🚀 Executing flow: {self.config.name}")
        print(f"📄 Description: {self.config.description}")
        print(f"🔢 Version: {self.config.version}")
        print("=" * 50)
        
        results = {
            'flow_name': self.config.name,
            'steps_executed': [],
            'files_processed': {},
            'combined_context': ''
        }
        
        for i, step in enumerate(self.config.flow, 1):
            step_name = step.get('step', f'step_{i}')
            step_type = step.get('type', 'unknown')
            file_path = step.get('file', '')
            description = step.get('description', 'No description')
            required = step.get('required', True)
            
            print(f"\n📋 Step {i}: {step_name}")
            print(f"   Type: {step_type}")
            print(f"   File: {file_path}")
            print(f"   Description: {description}")
            print(f"   Required: {required}")
            
            try:
                # Process the file if it exists
                full_path = self.base_path / file_path
                if full_path.exists():
                    processed_file = self.read_file(full_path)
                    results['files_processed'][step_name] = processed_file
                    results['steps_executed'].append({
                        'step': step_name,
                        'type': step_type,
                        'file': file_path,
                        'status': 'success',
                        'content_length': len(processed_file.content)
                    })
                    print(f"   ✅ Processed successfully ({len(processed_file.content)} chars)")
                else:
                    if required:
                        print(f"   ❌ Required file not found: {file_path}")
                        results['steps_executed'].append({
                            'step': step_name,
                            'type': step_type,
                            'file': file_path,
                            'status': 'error',
                            'error': 'File not found'
                        })
                    else:
                        print(f"   ⚠️  Optional file not found: {file_path}")
                        results['steps_executed'].append({
                            'step': step_name,
                            'type': step_type,
                            'file': file_path,
                            'status': 'skipped',
                            'reason': 'Optional file not found'
                        })
                        
            except Exception as e:
                print(f"   ❌ Error processing step: {e}")
                results['steps_executed'].append({
                    'step': step_name,
                    'type': step_type,
                    'file': file_path,
                    'status': 'error',
                    'error': str(e)
                })
        
        # Generate combined context for prompt files
        prompt_files = [f for f in results['files_processed'].values() 
                       if f.metadata.file_type == FileType.PROMPT]
        
        if prompt_files:
            results['combined_context'] = self.append_and_print_prompt_context(prompt_files)
        
        print(f"\n✅ Flow execution completed: {len(results['steps_executed'])} steps processed")
        return results
    
    def _execute_default_flow(self) -> Dict[str, any]:
        """Execute default behavior when no config is provided"""
        return {'flow_name': 'default', 'files_processed': self.read_all_files()}
    
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


def parse_args():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="GitHub Copilot Playbook - Prompt Flow Reader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python unit_test_prompt_flow.py --flow unit_test_flow.yaml
  python unit_test_prompt_flow.py --flow ../configs/my_flow.yaml --base-path ./workspace
  python unit_test_prompt_flow.py  # Run with default behavior
        """
    )
    
    parser.add_argument(
        '--flow',
        type=str,
        help='Path to YAML flow configuration file (e.g., unit_test_flow.yaml)'
    )
    
    parser.add_argument(
        '--base-path',
        type=str,
        default=None,
        help='Base directory path for file operations (default: current directory)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be executed without actually processing files'
    )
    
    return parser.parse_args()

def main():
    """
    Main entry point with CLI argument support
    """
    args = parse_args()
    
    print("🚀 GitHub Copilot Playbook - Prompt Flow Reader")
    print("=" * 60)
    
    # Load configuration if provided
    config = None
    if args.flow:
        try:
            config_path = Path(args.flow)
            if not config_path.is_absolute():
                config_path = Path.cwd() / config_path
            
            print(f"📄 Loading configuration from: {config_path}")
            config = PromptFlowReader.load_config(config_path)
            print(f"✅ Configuration loaded: {config.name} v{config.version}")
            
            if args.verbose:
                print(f"   Description: {config.description}")
                print(f"   Flow steps: {len(config.flow)}")
                
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"❌ Error loading configuration: {e}")
            return 1
    
    # Initialize reader
    try:
        reader = PromptFlowReader(base_path=args.base_path, config=config)
        
        if args.dry_run:
            print("\n🔍 DRY RUN MODE - No files will be processed")
            if config and config.flow:
                print("\nFlow steps that would be executed:")
                for i, step in enumerate(config.flow, 1):
                    step_name = step.get('step', f'step_{i}')
                    file_path = step.get('file', 'N/A')
                    print(f"  {i}. {step_name}: {file_path}")
            return 0
        
        # Execute flow or default behavior
        if config:
            results = reader.execute_flow()
            
            # Save results if configured
            if config.output.get('format') == 'combined' and results.get('combined_context'):
                output_file = reader.base_path / "combined_prompt_context.md"
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(results['combined_context'])
                    print(f"\n💾 Combined context saved to: {output_file}")
                except IOError as e:
                    print(f"\n❌ Failed to save combined context: {e}")
            
        else:
            # Default behavior - read all files
            print("\n📂 Running in default mode (no flow configuration)")
            all_files = reader.read_all_files()
            
            # Display summary
            for category, files in all_files.items():
                print(f"\n📁 {category.upper()} ({len(files)} files)")
                print("-" * 30)
                
                if args.verbose:
                    for processed_file in files:
                        reader.print_file_summary(processed_file)
                else:
                    # Show only file names in non-verbose mode
                    for processed_file in files:
                        print(f"   📄 {processed_file.file_path.name}")
            
            print(f"\n✅ Total files processed: {sum(len(files) for files in all_files.values())}")
            
            # Process prompts
            prompt_files = all_files.get('prompts', [])
            if prompt_files:
                combined_prompt_context = reader.append_and_print_prompt_context(prompt_files)
                
                # Save combined context
                output_file = reader.base_path / "combined_prompt_context.md"
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(combined_prompt_context)
                    print(f"\n💾 Combined prompt context saved to: {output_file}")
                except IOError as e:
                    print(f"\n❌ Failed to save combined context: {e}")
            else:
                print("\n🚫 No prompt files found to combine.")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)