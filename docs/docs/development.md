# Development

Development Infrastructure and Workflow

## CI/CD

- Automatic dependency updates and security alerts using GitHub Dependabot

**Github Actions**

- Project security analysis with Snyk
- Code quality analysis with CodeRabbit
- Frontend testing with Selenium
- Backend testing with the Django test framework
- Build the application as a Docker image and publish it to the GitHub Container Registry on pushes to main or on releases

## IDE

- At the beginning, I used Codium with Vim and Python extensions
- Later, I switched to Zed to try speeding up my workflow with an integrated LLM chat and better keyboard shortcut customization

## Git Workflow

The project is hosted on GitHub, and development is done using a feature-branch workflow based on relevant issues.

## HTTP Request Testing

ZAP was used to manipulate and analyze HTTP requests, for example for XSS testing and general traffic inspection.

## AI Usage

- Because the project is open source and not behind a legal wall, I am not concerned about sharing the code with AI companies.  
- I used a combination of ChatGPT via its web interface and various LLMs through the integrated chat, trying ChatGPT 5.2, Claude Opus 4.5, and Gemini 2.5 Flash.
- To protect myself, I disabled terminal access and file deletion functionality due to possible prompt injection via web search.  
- I also reviewed every code output for potential vulnerabilities and prompted with secure design in mind
