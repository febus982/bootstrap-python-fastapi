class ApplicationError(Exception):
    code: str
    internal_message: str
    public_message: str
    metadata: dict | None

    def __init__(self, code: str, internal_message: str, public_message: str, metadata: dict | None = None):
        """
        Represents an object encapsulating error information with attributes for code,
        internal message, public message, and optional metadata.

        Attributes:
        code (str): A short, unique, and descriptive code identifying the error.
        internal_message (str): A detailed message intended for internal use or logging purposes.
        public_message (str): A user-friendly message describing the error, suitable for public display.
        metadata (dict | None): Optional additional internal information or context regarding the error.

        Parameters:
        code: A short string representing the unique error code.
        internal_message: A string message containing the internal details of the error.
        public_message: A string message intended to be displayed to end users.
        metadata: An optional dictionary containing extra information about the error.
        """
        self.code = code
        self.internal_message = internal_message
        self.public_message = public_message
        self.metadata = metadata
