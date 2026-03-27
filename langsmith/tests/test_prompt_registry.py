"""Tests for the prompt registry and versioning system."""

import pytest
from langchain_core.prompts import ChatPromptTemplate

from langsmith.prompts.prompt_registry import PromptRegistry, PromptVersion


@pytest.fixture
def registry() -> PromptRegistry:
    """Create a fresh PromptRegistry for each test."""
    return PromptRegistry()


@pytest.fixture
def sample_template() -> ChatPromptTemplate:
    """Create a sample ChatPromptTemplate for testing."""
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{question}"),
    ])


class TestPromptRegistration:
    """Tests for registering prompt templates."""

    def test_register_new_template(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """Registering a new name should create version 1."""
        # TODO: Implement
        # 1. Register a template with name "test"
        # 2. Assert returned version number is 1
        raise NotImplementedError

    def test_register_increments_version(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """Re-registering the same name should increment the version."""
        # TODO: Implement
        # 1. Register "test" twice
        # 2. Assert second registration returns version 2
        raise NotImplementedError

    def test_register_stores_description(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """The description should be stored with the version."""
        # TODO: Implement
        raise NotImplementedError


class TestPromptRetrieval:
    """Tests for retrieving prompt templates."""

    def test_get_latest_version(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """get() without a version should return the latest."""
        # TODO: Implement
        raise NotImplementedError

    def test_get_specific_version(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """get() with a version number should return that exact version."""
        # TODO: Implement
        raise NotImplementedError

    def test_get_nonexistent_name_raises(self, registry: PromptRegistry) -> None:
        """get() with an unknown name should raise KeyError."""
        # TODO: Implement
        raise NotImplementedError

    def test_get_nonexistent_version_raises(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """get() with an unknown version number should raise KeyError."""
        # TODO: Implement
        raise NotImplementedError

    def test_get_template_returns_chat_prompt(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """get_template() should return the ChatPromptTemplate directly."""
        # TODO: Implement
        raise NotImplementedError


class TestPromptListing:
    """Tests for listing templates and versions."""

    def test_list_names_empty(self, registry: PromptRegistry) -> None:
        """An empty registry should return an empty list."""
        # TODO: Implement
        raise NotImplementedError

    def test_list_names_sorted(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """list_names() should return names in sorted order."""
        # TODO: Implement
        raise NotImplementedError

    def test_list_versions(
        self, registry: PromptRegistry, sample_template: ChatPromptTemplate
    ) -> None:
        """list_versions() should return all versions oldest first."""
        # TODO: Implement
        raise NotImplementedError

    def test_list_versions_unknown_name(self, registry: PromptRegistry) -> None:
        """list_versions() with unknown name should raise KeyError."""
        # TODO: Implement
        raise NotImplementedError


class TestLoadDefaults:
    """Tests for loading default templates."""

    def test_load_defaults_populates_registry(self, registry: PromptRegistry) -> None:
        """load_defaults() should register the standard templates."""
        # TODO: Implement
        # 1. Call registry.load_defaults()
        # 2. Assert "concise", "detailed", "step_by_step" are registered
        raise NotImplementedError
