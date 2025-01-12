from setuptools import setup

setup(
    name="travel_router",
    version="0.1.0",
    packages=[
        "feature",
        "feature.trip",
        "feature.sql",
        "feature.retrieval",
        "feature.llm",
        "feature.line",
    ],
    install_requires=[
        "googlemaps",
        "pandas",
        "pydantic",
        "requests",
        "python-dotenv",
        "openai",
        "qdrant-client",
    ],
    python_requires=">=3.12",
)
