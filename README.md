# Standalone Tailwind CSS CLI, installable via pip

Use *Tailwind CSS* without *Node.js* and install it via pip.

## Why

*Tailwind CSS* is notoriously dependent on *Node.js*. If you're a *Python* developer, this dependency may not be welcome
in your team, your Docker container, or your inner circle.

The *Tailwind CSS* team recently announced a new standalone CLI build that gives you the full power of *Tailwind CLI* in
a self-contained executable — no *Node.js* or `npm` required.

However, installing such a standalone CLI isn't as easy as running `npm install`, the installation command for *Node.js*
.

That's why I decided to make it as simple as running `pip install` command. As a result you can install the standalone *
Tailwind CLI* via `pip` by running the following command:

```bash
pip install pytailwindcss
```

Now you can run `tailwindcss` in your terminal as:

```
tailwindcss -i input.css -o output.css --minify
```

Voila!

## Get started

1. Install `tailwindcss` via `pip` by executing the following command:

   ```
   pip install pytailwindcss
   ```

2. [Optional] Preinstall `tailwindcss` binary by running the following command:

   ```
   tailwindcss_install
   ```

   If you skip this step, the binary will be downloaded on the first run of `tailwindcss` command.

3. The `tailwindcss` command should now be available in your terminal. Try to run it:

   ```
   tailwindcss
   ```

   If the installation was successful, you should see the message about binary being downloaded on the first run. When download is complete, you should see the help output for the `tailwindcss` command. Use `tailwindcss`
   to create a new project or work with an existing *Tailwind CSS* project.

4. Let's create a new project. Go to the directory where you want to host your *Tailwind CSS* project and initialize it
   by running:

   ```
   tailwindcss init
   ```

   This command will create the default *tailwind.config.js* file.

5. Start a watcher by running:

   ```
   tailwindcss -i input.css -o output.css --watch
   ```

6. Compile and minify your CSS for production by running:

   ```
   tailwindcss -i input.css -o output.css --minify
   ```

You got it. Please refer to [official Tailwind documentation](https://tailwindcss.com/docs) for more information on
using *Tailwind CSS* and its CLI.

## Caveats

It's not all roses, though. Giving up *Node.js* means you won't be able to install plugins or additional dependencies for
your *Tailwind CSS* setup. At the same time, that might not be a dealbreaker. You can still customize *Tailwind CSS* via
the *tailwind.config.js* file. And the standalone build also comes with all official *Tailwind CSS* plugins
like `@tailwindcss/aspect-ratio`, `@tailwindcss/forms`, `@tailwindcss/line-clamp`, and `@tailwindcss/typography`. So in
90% of *Tailwind CSS* usage cases you should be covered, and the setup is so simplified now.

Here is what the *Tailwind CSS* team says about going the standalone *Tailwind CSS* route:
> If you’re working on a project where you don’t otherwise need *Node.js* or `npm`, the standalone build can be a great choice. If Tailwind was the only reason you had a package.json file, this is probably going to feel like a nicer solution.

## Bugs and suggestions

If you have found a bug, please use the issue tracker on GitHub.

[https://github.com/timonweb/pytailwindcss/issues](https://github.com/timonweb/pytailwindcss/issues)

2021 (c) [Tim Kamanin - A Full Stack Django and Wagtail Developer](https://timonweb.com)
