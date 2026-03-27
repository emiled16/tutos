"""Prompt template management and versioning.

Provides a registry for storing, retrieving, and versioning prompt templates
so that different strategies can be compared systematically.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from langchain_core.prompts import ChatPromptTemplate


@dataclass(frozen=True)
class PromptVersion:
    """A versioned snapshot of a prompt template.

    Attributes:
        name: The template name (e.g., "concise", "detailed").
        version: Monotonically increasing version number.
        template: The actual ChatPromptTemplate.
        description: Human-readable description of what changed.
        created_at: Timestamp of creation.
    """

    name: str
    version: int
    template: ChatPromptTemplate
    description: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PromptRegistry:
    """Registry for managing versioned prompt templates.

    Stores multiple named prompt templates, each with a version history.
    Supports registering new versions, retrieving specific versions,
    and listing all available templates.
    """

    def __init__(self) -> None:
        self._registry: dict[str, list[PromptVersion]] = {}

    def register(
        self,
        name: str,
        template: ChatPromptTemplate,
        description: str = "",
    ) -> PromptVersion:
        """Register a new version of a prompt template.

        If the name already exists, increments the version number.
        Otherwise, creates version 1.

        Args:
            name: Template identifier (e.g., "concise", "detailed").
            template: The ChatPromptTemplate to register.
            description: What changed in this version.

        Returns:
            The created PromptVersion.
        """
        # TODO: Implement
        # 1. Determine the next version number for this name
        # 2. Create a PromptVersion instance
        # 3. Append to the registry
        # 4. Return the new version
        raise NotImplementedError

    def get(
        self,
        name: str,
        version: int | None = None,
    ) -> PromptVersion:
        """Retrieve a prompt template by name and optional version.

        Args:
            name: The template name.
            version: Specific version number. If None, returns the latest.

        Returns:
            The matching PromptVersion.

        Raises:
            KeyError: If the name or version is not found.
        """
        # TODO: Implement
        # 1. Look up the name in the registry
        # 2. If version is None, return the latest version
        # 3. Otherwise, find the specific version number
        # 4. Raise KeyError with a descriptive message if not found
        raise NotImplementedError

    def get_template(
        self,
        name: str,
        version: int | None = None,
    ) -> ChatPromptTemplate:
        """Convenience method to get just the ChatPromptTemplate.

        Args:
            name: The template name.
            version: Optional version number.

        Returns:
            The ChatPromptTemplate for the specified version.
        """
        # TODO: Implement
        raise NotImplementedError

    def list_names(self) -> list[str]:
        """Return all registered template names.

        Returns:
            Sorted list of template names.
        """
        # TODO: Implement
        raise NotImplementedError

    def list_versions(self, name: str) -> list[PromptVersion]:
        """Return all versions of a named template.

        Args:
            name: The template name.

        Returns:
            List of PromptVersion objects, oldest first.

        Raises:
            KeyError: If the name is not found.
        """
        # TODO: Implement
        raise NotImplementedError

    def load_defaults(self) -> None:
        """Load the default set of prompt templates into the registry.

        Registers the concise, detailed, and step-by-step templates
        from the templates module.
        """
        # TODO: Implement
        # Import templates from langsmith.prompts.templates and register each one
        raise NotImplementedError
