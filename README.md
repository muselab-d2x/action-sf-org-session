# Secure Salesforce Authentication GitHub Action

This GitHub Action securely accesses the `SFDX_AUTH_URL` and exchanges it for an `ACCESS_TOKEN` and `INSTANCE_URL` using the `d2x` package. It uses the `GITHUB_TOKEN` from a GitHub App with Environment Management permissions to create a new session ephemeral environment.

## Usage

To use this action in your workflow, add the following steps to your `.github/workflows/main.yml` file:

```yaml
jobs:
  example-job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Secure Salesforce Authentication
        uses: githubnext/workspace-blank@main
        with:
          SFDX_AUTH_URL: ${{ secrets.SFDX_AUTH_URL }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name          | Description                                             | Required |
|---------------|---------------------------------------------------------|----------|
| `SFDX_AUTH_URL` | The Salesforce authentication URL.                      | true     |
| `GITHUB_TOKEN`  | The GitHub token with Environment Management permissions. | true     |

## Outputs

None

## Session Management and Cleanup

This action includes logic to manage sessions for accessing Salesforce credentials. When a session is ended, it triggers logic to revoke the Salesforce grant and delete the session environment from GitHub.

To end a session, set a flag in your workflow to trigger the cleanup logic. The action will then revoke the Salesforce grant and delete the session environment.
