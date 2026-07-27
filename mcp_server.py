from fastmcp import FastMCP
from pathlib import Path
from src.parser import parse_file

# Create an MCP server
mcp = FastMCP("Aviation Accident Analysis")

PROMPTS_DIR = Path("prompts")

@mcp.tool()
def upload_and_generate_prompt(file_path: str, template_name: str = "extract_entities") -> str:
    """
    Upload an aviation accident report (PDF, DOCX, TXT), parse it, 
    and wrap it in a specified prompt template.
    
    :param file_path: Path to the document file.
    :param template_name: Name of the template in the prompts/ directory (e.g., 'extract_entities').
    :return: The generated prompt ready for LLM input.
    """
    try:
        # Parse the document
        content = parse_file(file_path)
        
        # Load the template
        template_path = PROMPTS_DIR / f"{template_name}.txt"
        if not template_path.exists():
            available_templates = [f.stem for f in PROMPTS_DIR.glob("*.txt")]
            return f"Error: Template '{template_name}' not found. Available templates: {', '.join(available_templates)}"
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Inject content into template
        # Standard placeholder in this project seems to be {input_text}
        if "{input_text}" in template:
            prompt = template.replace("{input_text}", content)
        else:
            # Fallback: append content if no placeholder found
            prompt = f"{template}\n\n[DOCUMENT CONTENT]:\n{content}"
            
        return prompt
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_available_templates() -> list[str]:
    """
    List all available prompt templates in the prompts/ directory.
    """
    return [f.stem for f in PROMPTS_DIR.glob("*.txt")]

@mcp.tool()
def list_available_reports(directory: str = "input") -> list[str]:
    """
    List all available reports in a specified directory.
    """
    report_dir = Path(directory)
    if not report_dir.exists():
        return []
    return [f.name for f in report_dir.iterdir() if f.is_file() and f.suffix.lower() in [".pdf", ".docx", ".txt"]]

if __name__ == "__main__":
    mcp.run()
