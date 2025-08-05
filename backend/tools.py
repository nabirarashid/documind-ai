from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class ToolType(Enum):
    PAYMENT = "payment"
    UI_FRAMEWORK = "ui_framework"
    JS_FRAMEWORK = "js_framework"
    DEPLOYMENT = "deployment"
    DATABASE = "database"
    STYLING = "styling"

@dataclass
class ToolConfig:
    name: str
    tool_type: ToolType
    base_url: str
    scrape_paths: List[str]
    selectors: Dict[str, str]  # CSS selectors for content extraction
    max_depth: int = 2
    delay: float = 1.0
    enabled: bool = True

# Tool configurations
TOOLS = {
    "stripe": ToolConfig(
        name="Stripe",
        tool_type=ToolType.PAYMENT,
        base_url="https://stripe.com/",
        scrape_paths=[
            "/docs/api",
            "/docs/payments",
            "/docs/connect",
            "/docs/billing",
            "/docs/checkout"
        ],
        selectors={
            "content": "article, .docs-content, main",
            "title": "h1, .page-title",
            "exclude": ".sidebar, .navigation, .footer"
        }
    ),
    
    "tailwind": ToolConfig(
        name="Tailwind CSS",
        tool_type=ToolType.STYLING,
        base_url="https://tailwindcss.com",
        scrape_paths=[
            "/docs/installation/using-vite",
            "/docs/utility-first",
            "/docs/responsive-design",
            "/docs/hover-focus-and-other-states",
            "/docs/dark-mode",
            "/docs/columns",
            "/docs/gap",
            "/docs/flex-direction",
            "/docs/flex-wrap",
            "/docs/padding",
            "/docs/margin",
            "/docs/text-color",
            "/docs/content",
            "/docs/border-style",
            "/docs/backdrop-filter",
            "/docs/transition-property"
        ],
        selectors={
            "content": ".prose, article, main",
            "title": "h1, h2",
            "exclude": ".sidebar, nav, .banner"
        }
    ),
    
    "react": ToolConfig(
        name="React",
        tool_type=ToolType.JS_FRAMEWORK,
        base_url="https://react.dev",
        scrape_paths=[
            "/learn",
            "/reference/react",
            "/reference/react-dom",
            "/learn/installation",
            "/learn/start-a-new-react-project",
            "/learn/thinking-in-react",
            "/learn/describing-the-ui",
            "/learn/adding-interactivity",
            "/learn/managing-state",
            "/learn/escape-hatches"
        ],
        selectors={
            "content": "article, .content, main",
            "title": "h1, h2",
            "exclude": "nav, .sidebar, footer"
        }
    ),
    
    "vercel": ToolConfig(
        name="Vercel",
        tool_type=ToolType.DEPLOYMENT,
        base_url="https://vercel.com",
        scrape_paths=[
            "/docs/projects",
            "/docs/deployments",
            "/docs/functions",
            "/docs/storage",
            "/docs/frameworks",
            "/docs/cli"
        ],
        selectors={
            "content": ".prose, article, main",
            "title": "h1, h2",
            "exclude": ".sidebar, nav, .footer"
        }
    ),
    
    "nextjs": ToolConfig(
        name="Next.js",
        tool_type=ToolType.JS_FRAMEWORK,
        base_url="https://nextjs.org",
        scrape_paths=[
            "/docs/getting-started/installation",
            "/docs/pages/building-your-application",
            "/docs/app/building-your-application",
            "/docs/app/api-reference/cli",
            "/docs/app/api-reference/components/script",
            "/docs/pages/api-reference/create-next-app"
        ],
        selectors={
            "content": "article, .nextra-content, main",
            "title": "h1, h2",
            "exclude": "nav, .sidebar, footer"
        }
    )
}

def get_tool_config(tool_name: str) -> Optional[ToolConfig]:
    """Get configuration for a specific tool"""
    return TOOLS.get(tool_name.lower())

def get_enabled_tools() -> Dict[str, ToolConfig]:
    """Get all enabled tools"""
    return {name: config for name, config in TOOLS.items() if config.enabled}

def get_tools_by_type(tool_type: ToolType) -> Dict[str, ToolConfig]:
    """Get tools filtered by type"""
    return {name: config for name, config in TOOLS.items() 
            if config.tool_type == tool_type and config.enabled}