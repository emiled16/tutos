"""LangSmith dataset management utilities.

Create, upload, and manage evaluation datasets in LangSmith for
systematic testing of LLM applications.
"""

from dataclasses import dataclass

from langsmith import Client


@dataclass
class QAExample:
    """A single question-answer pair for evaluation.

    Attributes:
        question: The input question.
        context: The context documents provided to the chain.
        expected_answer: The ground truth / reference answer.
        metadata: Optional metadata tags for filtering.
    """

    question: str
    context: list[str]
    expected_answer: str
    metadata: dict[str, str] | None = None


class DatasetManager:
    """Manages LangSmith datasets for LLM evaluation.

    Provides methods to create datasets, add examples, and retrieve
    datasets for use in evaluation runs.
    """

    def __init__(self, client: Client | None = None) -> None:
        """Initialize with an optional LangSmith client.

        Args:
            client: A LangSmith Client. Creates a default one if not provided.
        """
        # TODO: Implement — store or create the LangSmith client
        raise NotImplementedError

    def create_dataset(
        self,
        name: str,
        description: str = "",
    ) -> str:
        """Create a new dataset in LangSmith.

        Args:
            name: Unique name for the dataset.
            description: Human-readable description.

        Returns:
            The dataset ID as a string.
        """
        # TODO: Implement
        # 1. Use self.client.create_dataset(name, description=description)
        # 2. Return the dataset ID
        raise NotImplementedError

    def add_examples(
        self,
        dataset_name: str,
        examples: list[QAExample],
    ) -> int:
        """Add QA examples to an existing dataset.

        Args:
            dataset_name: Name of the target dataset.
            examples: List of QAExample instances to add.

        Returns:
            The number of examples added.
        """
        # TODO: Implement
        # 1. For each QAExample, construct input and output dicts
        # 2. Use self.client.create_examples(inputs=..., outputs=..., dataset_name=...)
        # 3. Return the count
        raise NotImplementedError

    def create_dataset_from_csv(
        self,
        name: str,
        csv_path: str,
        question_col: str = "question",
        context_col: str = "context",
        answer_col: str = "expected_answer",
    ) -> str:
        """Create a dataset from a CSV file.

        Args:
            name: Name for the new dataset.
            csv_path: Path to the CSV file.
            question_col: Column name for questions.
            context_col: Column name for context (JSON-encoded list).
            answer_col: Column name for expected answers.

        Returns:
            The dataset ID.
        """
        # TODO: Implement
        # 1. Read the CSV file
        # 2. Parse each row into a QAExample
        # 3. Create the dataset and add examples
        raise NotImplementedError

    def list_datasets(self) -> list[dict[str, str]]:
        """List all datasets in the LangSmith project.

        Returns:
            List of dicts with keys "id", "name", "description", "example_count".
        """
        # TODO: Implement
        raise NotImplementedError

    def delete_dataset(self, name: str) -> bool:
        """Delete a dataset by name.

        Args:
            name: The dataset name to delete.

        Returns:
            True if deleted, False if not found.
        """
        # TODO: Implement
        raise NotImplementedError
