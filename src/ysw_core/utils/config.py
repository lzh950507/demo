from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="YSW",
    settings_files=["config/settings.yaml"],
    environments=True,
    load_dotenv=True,
    env_switcher="YSW_ENV"
)