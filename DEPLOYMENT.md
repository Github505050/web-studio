# Deployment — One new repo, no existing projects touched

The current connected GitHub app cannot create repositories. To allow ChatGPT to publish this code through the connected GitHub tool, create a **new** repository in the browser:

1. Open <https://github.com/new> while signed in as `Github505050`.
2. Repository name: **web-studio**.
3. Choose **Public**.
4. Select **Add a README** so the repository has an initialized `main` branch.
5. Click **Create repository**.
6. Return to the chat and say **"Created web-studio. Upload the website."**

The GitHub connector can then write to the new repository without changing `Portfolio`, `french-classroom` or `northline-support`.

Alternatively, extract the provided ZIP locally, upload its **contents** to the new repository, and enable Pages:

**Settings → Pages → Deploy from a branch → main → /(root) → Save**.

Expected published URL after a successful deployment: `https://github505050.github.io/web-studio/`. This URL is an expected path, **not** a confirmed live site until GitHub Pages reports a completed deployment.
