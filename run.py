import argparse
import os
import sys
from pathlib import Path
import uvicorn

# Ensure src directory is in python path
src_path = Path(__file__).resolve().parent / "src"
sys.path.append(str(src_path))

def main():
    parser = argparse.ArgumentParser(description="Run the FastDemo application.")
    parser.add_argument(
        "--env", 
        default="development", 
        help="Environment to run in (default, development, production). Default is development."
    )
    args = parser.parse_args()

    # Set environment variable for Dynaconf BEFORE loading settings
    os.environ["ENV_FOR_DYNACONF"] = args.env
    print(f"🚀 Starting application in '{args.env}' environment...")

    try:
        # Import settings after setting environment variable
        from ysw_core.utils.config import settings
        
        # Determine reload status based on settings or defaults
        # Note: In settings.yaml, we have 'reload' key in dev/prod
        should_reload = settings.get("reload", False)
        host = settings.get("host", "0.0.0.0")
        port = settings.get("port", 48180)

        print(f"🔧 Config: Debug={settings.get('DEBUG', False)}, Reload={should_reload}")

        uvicorn.run(
            "ysw_web.main:app",
            host=host,
            port=port,
            reload=should_reload
        )
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        print("Ensure you are running from the project root and dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
