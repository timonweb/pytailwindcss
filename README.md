# Standalone Tailwind CSS CLI, installable via pip

Use *Tailwind CSS* without *Node.js* — install it via pip.

## Why

*Tailwind CSS* is notoriously dependent on *Node.js*. If you're a *Python* developer, this dependency may not be welcome
in your team, your Docker container, or your inner circle.

The *Tailwind CSS* team recently announced a new standalone CLI build that gives you the full power of *Tailwind CLI* in
a self-contained executable — no *Node.js* or `npm` required.

However, installing the standalone CLI isn't as easy as running `npm install`.

That's why I created this package to make it as simple as running the `pip install` command. Now you can install the standalone *Tailwind CLI* via `pip` by running:

```bash
pip install pytailwindcss
```

Now you can run `tailwindcss` in your terminal:

```bash
tailwindcss -i input.css -o output.css --minify
```

Voilà!

## Get started

1. Install `pytailwindcss` via `pip`:

   ```bash
   pip install pytailwindcss
   ```

2. **[Recommended]** Preinstall the `tailwindcss` binary:

   ```bash
   tailwindcss_install
   ```

   By default, the latest binary version will be downloaded. To pin to a specific Tailwind CSS version, set the `TAILWINDCSS_VERSION` environment variable before running the command:

   ```bash
   # In a Dockerfile
   ENV TAILWINDCSS_VERSION=v4.1.16
   RUN tailwindcss_install

   # On Linux/macOS
   export TAILWINDCSS_VERSION=v4.1.16
   tailwindcss_install

   # On Windows (cmd)
   set TAILWINDCSS_VERSION=v4.1.16
   tailwindcss_install

   # On Windows (PowerShell)
   $env:TAILWINDCSS_VERSION="v4.1.16"
   tailwindcss_install
   ```

   To see a list of available Tailwind CSS releases, visit: https://github.com/tailwindlabs/tailwindcss/releases

   If you skip this step, the binary will be downloaded automatically on the first run of the `tailwindcss` command.

3. The `tailwindcss` command should now be available in your terminal. Try running it:

   ```bash
   tailwindcss
   ```

   You should see the help output for the `tailwindcss` command. If you skipped step 2, the binary will be downloaded automatically on this first run. Use `tailwindcss` to create a new project or work with an existing *Tailwind CSS* project.

4. Create a new *Tailwind CSS* project by navigating to your project directory and initializing it:

   ```bash
   tailwindcss init
   ```

   This command creates the default *tailwind.config.js* file.

5. Start a watcher to compile CSS automatically during development:

   ```bash
   tailwindcss -i input.css -o output.css --watch
   ```

6. Compile and minify your CSS for production:

   ```bash
   tailwindcss -i input.css -o output.css --minify
   ```

That's it! For more information on using *Tailwind CSS* and its CLI, refer to the [official Tailwind CSS documentation](https://tailwindcss.com/docs).

## Caveats

While this approach simplifies your setup, there are some trade-offs. Without *Node.js*, you won't be able to install third-party plugins or additional dependencies for your *Tailwind CSS* setup. However, this might not be a dealbreaker for most use cases.

You can still customize *Tailwind CSS* via the *tailwind.config.js* file, and the standalone build includes all official *Tailwind CSS* plugins: `@tailwindcss/aspect-ratio`, `@tailwindcss/forms`, `@tailwindcss/line-clamp`, and `@tailwindcss/typography`. This covers approximately 90% of typical *Tailwind CSS* usage scenarios.

Here's what the *Tailwind CSS* team says about the standalone build:
> If you're working on a project where you don't otherwise need *Node.js* or `npm`, the standalone build can be a great choice. If Tailwind was the only reason you had a package.json file, this is probably going to feel like a nicer solution.

## Bugs and Suggestions

Found a bug or have a suggestion? Please use the issue tracker on GitHub:

[https://github.com/timonweb/pytailwindcss/issues](https://github.com/timonweb/pytailwindcss/issues)

2021 - 2025 (c) Tim Kamanin — [A Full-Stack Django and Wagtail Developer](https://timonweb.com)
