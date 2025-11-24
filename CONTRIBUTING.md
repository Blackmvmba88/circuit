# Contributing to Circuit

Thank you for your interest in contributing to Circuit! We welcome contributions from everyone, whether you're fixing a typo, proposing a new feature, or building major tooling.

## How to Contribute

### 1. Find or Create an Issue

Before starting work, please:

- Check [existing issues](../../issues) to see if your idea or bug has been reported
- If not, create a new issue describing what you'd like to work on
- Wait for feedback from maintainers to ensure alignment with project goals

### 2. Fork and Clone

1. Fork the repository to your GitHub account
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/circuit.git
   cd circuit
   ```

### 3. Create a Branch

Create a branch for your work:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Your Changes

- Keep changes focused and atomic
- Follow existing code style and conventions
- Write clear commit messages
- Add or update tests if applicable
- Update documentation as needed

### 5. Test Your Changes

Before submitting:

- Test your changes thoroughly
- Ensure any examples work as expected
- Run linters/validators if available

### 6. Submit a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a Pull Request against the `main` branch
3. Fill out the PR template with:
   - Clear description of changes
   - Link to related issue(s)
   - Any testing performed
   - Screenshots if applicable

### 7. Code Review

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged!

## Areas for Contribution

We welcome contributions in several areas:

### Format Specification
- Help define the `.circuit.json` schema
- Propose improvements to the format
- Document format specifications

### Tooling
- Build validators for circuit files
- Create converters to/from other formats
- Develop visualizers and editors

### Adapters
- Create adapters for popular EDA tools (KiCad, EAGLE, etc.)
- Build export/import functionality

### Documentation
- Improve README and guides
- Write tutorials and examples
- Create reference documentation

### Examples
- Contribute example circuits
- Document common circuit patterns
- Create educational content

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## Style Guidelines

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Provide detailed description in body if needed
- Reference issue numbers when applicable

### Code Style

- Follow existing conventions in the codebase
- Keep code readable and well-commented
- Prioritize clarity over cleverness

### Documentation

- Use clear, concise language
- Provide examples where helpful
- Keep documentation up-to-date with code changes

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the `question` label
- Start a discussion in [GitHub Discussions](../../discussions)
- Reach out to maintainers

Thank you for contributing to Circuit! 🎉
