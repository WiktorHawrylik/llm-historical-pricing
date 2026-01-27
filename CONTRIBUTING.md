# Contributing to LLM Historical Pricing

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/llm-historical-pricing.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`

## Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_wayback_pricing.py

# Run examples
python examples.py
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

## Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Add integration tests when possible
- Test with actual Wayback Machine API when appropriate

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update QUICK_REFERENCE.md if you add new commands or options
3. Add examples to examples.py if you add new functionality
4. Ensure tests pass
5. Update the version number if applicable

## Ideas for Contributions

Here are some areas where contributions would be valuable:

### Features
- **Data parsing**: Extract actual pricing data from archived HTML pages
- **Price comparison**: Automated comparison between different time periods
- **Export formats**: JSON, CSV, or Excel export of pricing data
- **Visualization**: Charts showing pricing trends over time
- **Caching**: Local caching of snapshots to reduce API calls
- **More providers**: Support for Anthropic, Google, etc.

### Improvements
- **Better error handling**: More informative error messages
- **Progress indicators**: Show progress for long-running operations
- **Concurrent fetching**: Fetch multiple snapshots in parallel
- **Configuration file**: Allow custom settings via config file
- **Retry logic**: Automatic retry with exponential backoff

### Documentation
- **Video tutorial**: Screen recording of basic usage
- **Use cases**: Real-world examples of pricing analysis
- **API documentation**: Detailed API reference
- **Troubleshooting**: Common issues and solutions

## Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Full error message and stack trace
- Steps to reproduce
- Expected vs actual behavior

## Feature Requests

When requesting features, please:
- Describe the use case
- Explain the expected behavior
- Provide examples if possible
- Consider implementation complexity

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## License

By contributing, you agree that your contributions will be subject to the same license as the project.
