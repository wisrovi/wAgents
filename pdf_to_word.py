#!/usr/bin/env python3
"""
Simple PDF to Word converter for wAgents documentation
Creates a basic Word document with content from PDF
"""

import sys
import os

def create_word_document():
    """Create a basic Word document with wAgents documentation content"""
    
    # Create a new Word document
    doc = Document()
    
    # Add title
    doc.add_heading('wAgents: AI Agent Development Environment', level=0)
    doc.add_paragraph('Comprehensive Docker-based Development Platform for Modern AI Applications')
    
    # Add hero section
    doc.add_heading('INSTANT BOOTSTRAP - ONE COMMAND TO RULE THEM ALL', level=1)
    doc.add_paragraph('Copy and Paste This Alias:')
    
    # Add the alias in a code block
    alias_code = '''alias wisrovi="docker run --rm --hostname wAgent --init -i -t --shm-size=16g --cpus 6.0 --memory 16g --gpus all --log-opt max-size=50m -e TZ=Europe/Madrid -v \"$(pwd)\":/app -v /var/run/docker.sock:/var/run/docker.sock -v ~/.ssh:/root/.ssh:ro wisrovi/agents:gpu-slim zsh"'''
    doc.add_code(alias_code)
    
    doc.add_paragraph('Then simply run: wisrovi')
    
    # Add benefits section
    doc.add_heading('WHAT YOU GET INSTANTLY:', level=1)
    benefits = [
        '• GPU Acceleration - CUDA 12.0 ready',
        '• Security Tools - Bandit, Safety scanners',
        '• Code Quality - Ruff, pre-commit hooks',
        '• AI/ML Stack - YOLO, PyTorch, OpenCV',
        '• Productivity - Zsh, 20+ dev tools',
        '• Data Management - DVC with S3 support'
    ]
    
    for benefit in benefits:
        doc.add_paragraph(benefit)
    
    # Add why section
    doc.add_heading('WHY THIS IS GAME-CHANGER:', level=1)
    advantages = [
        '• Zero Setup Time - No environment configuration',
        '• Consistent Everywhere - Same setup on any machine',
        '• Production Ready - Battle-tested configuration',
        '• Resource Optimized - 16GB RAM, 6 CPUs, full GPU',
        '• Security First - Built-in vulnerability scanning',
        '• AI Optimized - Ready for ML workloads'
    ]
    
    for advantage in advantages:
        doc.add_paragraph(advantage)
    
    # Add conclusion
    doc.add_heading('THAT IS IT! YOU ARE READY TO BUILD AI AGENTS!', level=1)
    doc.add_paragraph('The rest of this documentation explains what you now have at your fingertips...')
    
    # Add author info
    doc.add_heading('Document Information:', level=1)
    doc.add_paragraph('Author: Wisrovi Rodriguez')
    doc.add_paragraph('Version: 1.0')
    doc.add_paragraph('Date: November 24, 2025')
    doc.add_paragraph('')
    doc.add_paragraph('Note: This is a simplified Word document with key bootstrap information.')
    doc.add_paragraph('For the full documentation, please refer to the PDF: wAgents_Documentation.pdf')
    
    return doc

def main():
    """Main function to create Word document"""
    try:
        doc = create_word_document()
        
        # Save the document
        doc.save('/app/wAgents_Documentation.docx')
        
        print("✅ Word document created successfully!")
        print("📄 File saved as: wAgents_Documentation.docx")
        print("📝 Note: This is a simplified Word document with key bootstrap information.")
        print("📚 For the full documentation, please refer to the PDF: wAgents_Documentation.pdf")
        
    except Exception as e:
        print(f"❌ Error creating Word document: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

def create_word_document():
    """Create a basic Word document with wAgents documentation content"""
    
    # Create a new Word document
    doc = Document()
    
    # Add title
    title = doc.add_heading('wAgents: AI Agent Development Environment', level=0)
    doc.add_paragraph('Comprehensive Docker-based Development Platform for Modern AI Applications')
    
    # Add hero section
    doc.add_heading('INSTANT BOOTSTRAP - ONE COMMAND TO RULE THEM ALL', level=1)
    doc.add_paragraph('Copy and Paste This Alias:')
    
    # Add the alias in a code block
    alias_code = '''alias wisrovi="docker run --rm --hostname wAgent --init -i -t --shm-size=16g --cpus 6.0 --memory 16g --gpus all --log-opt max-size=50m -e TZ=Europe/Madrid -v \"$(pwd)\\":/app -v /var/run/docker.sock:/var/run/docker.sock -v ~/.ssh:/root/.ssh:ro wisrovi/agents:gpu-slim zsh"'''
    doc.add_code(alias_code)
    
    doc.add_paragraph('Then simply run: wisrovi')
    
    # Add benefits section
    doc.add_heading('WHAT YOU GET INSTANTLY:', level=1)
    benefits = [
        '• GPU Acceleration - CUDA 12.0 ready',
        '• Security Tools - Bandit, Safety scanners',
        '• Code Quality - Ruff, pre-commit hooks',
        '• AI/ML Stack - YOLO, PyTorch, OpenCV',
        '• Productivity - Zsh, 20+ dev tools',
        '• Data Management - DVC with S3 support'
    ]
    
    for benefit in benefits:
        doc.add_paragraph(benefit)
    
    # Add why section
    doc.add_heading('WHY THIS IS GAME-CHANGER:', level=1)
    advantages = [
        '• Zero Setup Time - No environment configuration',
        '• Consistent Everywhere - Same setup on any machine',
        '• Production Ready - Battle-tested configuration',
        '• Resource Optimized - 16GB RAM, 6 CPUs, full GPU',
        '• Security First - Built-in vulnerability scanning',
        '• AI Optimized - Ready for ML workloads'
    ]
    
    for advantage in advantages:
        doc.add_paragraph(advantage)
    
    # Add conclusion
    doc.add_heading('THAT IS IT! YOU ARE READY TO BUILD AI AGENTS!', level=1)
    doc.add_paragraph('The rest of this documentation explains what you now have at your fingertips...')
    
    # Add author info
    doc.add_heading('Document Information:', level=1)
    doc.add_paragraph('Author: Wisrovi Rodriguez')
    doc.add_paragraph('Version: 1.0')
    doc.add_paragraph('Date: November 24, 2025')
    doc.add_paragraph('')
    doc.add_paragraph('Note: This is a simplified Word document with key bootstrap information.')
    doc.add_paragraph('For the full documentation, please refer to the PDF: wAgents_Documentation.pdf')
    
    return doc

def main():
    """Main function to create Word document"""
    try:
        doc = create_word_document()
        
        # Save the document
        doc.save('/app/wAgents_Documentation.docx')
        
        print("✅ Word document created successfully!")
        print("📄 File saved as: wAgents_Documentation.docx")
        print("📝 Note: This is a simplified Word document with key bootstrap information.")
        print("📚 For the full documentation, please refer to the PDF: wAgents_Documentation.pdf")
        
    except Exception as e:
        print(f"❌ Error creating Word document: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()