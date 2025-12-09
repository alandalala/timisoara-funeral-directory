# Contributing to Timișoara Funeral Directory

Thank you for your interest in contributing to this project! This guide will help you get started.

## Code of Conduct

This project aims to provide a valuable service to bereaved families. Please maintain a respectful and professional tone in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/timisoara-funeral-directory.git`
3. Follow the setup instructions in `SETUP.md`
4. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Workflow

### Backend (Python)

1. **Activate virtual environment:**
   ```bash
   cd backend
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Unix
   ```

2. **Make your changes**

3. **Test your changes:**
   ```bash
   pytest
   ```

4. **Check code style:**
   ```bash
   flake8 .
   black .
   ```

### Frontend (Next.js)

1. **Start development server:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Make your changes**

3. **Run linter:**
   ```bash
   npm run lint
   ```

4. **Build to check for errors:**
   ```bash
   npm run build
   ```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions and classes
- Use Pydantic for data validation
- Maximum line length: 100 characters

Example:
```python
def normalize_phone_number(phone: str) -> Tuple[str, str]:
    """
    Normalize Romanian phone number to E.164 format.
    
    Args:
        phone: Raw phone number string
    
    Returns:
        Tuple of (normalized_number, type)
    """
    # Implementation
```

### TypeScript/React

- Follow the existing code style
- Use functional components with hooks
- Use TypeScript strict mode
- Prefer named exports
- Use proper type annotations

Example:
```typescript
interface CompanyCardProps {
  company: Company;
  onCall?: () => void;
}

export function CompanyCard({ company, onCall }: CompanyCardProps) {
  // Implementation
}
```

## Commit Messages

Follow the Conventional Commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add service filtering to company search
fix: correct phone number normalization for landlines
docs: update setup instructions for Windows users
```

## Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update the CHANGELOG.md** with your changes
5. **Submit your PR** with a clear description:
   - What problem does it solve?
   - How did you solve it?
   - Any breaking changes?

### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How did you test these changes?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass
```

## Areas for Contribution

### High Priority

1. **Data Quality Improvements**
   - Better motto extraction algorithms
   - Improved address parsing
   - Enhanced DSP verification logic

2. **Frontend Components**
   - Advanced filtering UI
   - Mobile-optimized map view
   - Accessibility improvements

3. **Testing**
   - Unit tests for backend tools
   - E2E tests for frontend flows
   - Integration tests

### Medium Priority

1. **Features**
   - Multi-language support (Romanian/Hungarian)
   - User reviews and ratings
   - Price comparison tools

2. **Performance**
   - Database query optimization
   - Frontend bundle size reduction
   - Image optimization

### Documentation

- API documentation improvements
- Setup guides for different platforms
- Architecture decision records (ADRs)
- Translation of documentation

## Reporting Bugs

Use the GitHub issue tracker. Include:

1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Numbered steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: OS, browser, versions
6. **Screenshots**: If applicable
7. **Logs**: Relevant error messages

## Feature Requests

Open a GitHub issue with:

1. **Problem statement**: What problem does this solve?
2. **Proposed solution**: How would you implement it?
3. **Alternatives**: Other approaches considered
4. **Additional context**: Any other relevant info

## Questions?

- Open a GitHub Discussion for general questions
- Check existing issues and documentation first
- Be specific and provide context

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for helping make this project better! 🙏
