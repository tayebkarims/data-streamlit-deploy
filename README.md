# Deploying Streamlit

## 🎯 Objectives

You have a website running locally now, but no one else can access it. Unless something is fundamentally wrong with your machine's security of course. 😱

So, let's deploy your site to the cloud.

## 1) Methods to deploy the front-end

Think for a second about how you could do that. You already know at least one method to do it!

<details>
  <summary markdown='span'><strong> 💡 Answer </strong></summary>

  You could containerize our streamlit API: build a Docker image with Streamlit and your code.

  You'll explore an easier way to deploy it, although it is limited to small applications.

  If you ever need to deploy Streamlit with Docker, or want to try it out, have a look at the [official documentation](https://docs.streamlit.io/deploy/tutorials/docker). (Not now, only when you really need to.) The tutorial is well written. 👍

  <details>
    <summary markdown='span'><strong> You'd need a couple of tweaks though. </strong></summary>

  - The Streamlit documentation uses `pip` to install the requirements. Three options for you:
    - Translate your `pyproject.toml` into a `requirements.txt` file:
      ```bash
      uv pip compile -o requirements.txt --python-platform linux pyproject.toml
      ```
    - Change the code to use your `pyproject.toml` instead.
    - Replace the `RUN` commands with what we did to deploy our API with `uv`. (Install `uv`, and then `uv sync`.)
  - Google Cloud Run requires that your site runs on port `8080`. You'd have to change the default port from `8501` to `8080`.

  </details>

</details>

<br>

In this challenge, we'll take the easy route: deploy using **Streamlit Community Cloud**.


## 2) What do we need to deploy? (For a simple lightweight app.)

Let's setup the project for **Streamlit Community Cloud**.

❓ **What do we need to deploy the website to Streamlit Community Cloud ?**

<details>
  <summary markdown='span'><strong> 💡 Answer </strong></summary>

  - An account for Streamlit Community Cloud.
  - A GitHub repository with the code for our app.
  - A list of your dependencies in a format supported by Streamlit Community Cloud.

</details>

<br>

### 2.1) Create an account for Streamlit Community Cloud

👉 Go to [Streamlit Community Cloud](https://share.streamlit.io/) and create an account.

You can use any authentication method you want but using your GitHub account is the most efficient one as you will need access to your repository anyway. 😉

### 2.2) GitHub repository

You already have one, and you already pushed your code at the end of the previous challenge. 👍

### 2.3 Dependencies

Because you are using a modern dependency manager like `uv` to manage our dependencies, you already have a list of dependencies in your `pyproject.toml` (the base packages we need) and `uv.lock` (the resolved versions of all dependencies and their dependencies).

We are lucky: since 2024 Streamlit Community Cloud uses `uv` to install dependencies, and it supports the `uv.lock` file. It's actually the one it prioritizes if it finds one. ([Link to know more about the different formats Streamlit Community Cloud supports.](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies))

So, nothing to do: the `uv.lock` file is enough! 👍

## 3) Let's deploy

👉 Execute these steps:

1. Sign in to **Streamlit Community Cloud**.
1. Find the button to _Create an app_.
1. Choose _Deploy a public app from GitHub_.
1. Fill in the fields:
   - Select your repository.
   - Select the `master` branch.
   - Main file path is `app.py`.
   - App URL, choose `zoologist-<user.github_nickname>`.

Wait? You get an error, 'This file does not exist.'. How comes? Try to figure it out. Have a look at your GitHub repo.

<details>
  <summary markdown='span'><strong> 💡 Answer </strong></summary>

  Your code is not yet on the `master` branch. You pushed the feature branch, but never merged it into `master`.

</details>

Fix the problem, and then try to deploy your app again:

1. Fill in all the fields as described above. (Make sure to include your GitHub username in the app URL!)
1. Click on _Advanced settings_.
1. Change the Python version to the one you used locally. (Can't remember? `uv run python --version`.)
1. Click on _Save_.
1. Click on _Deploy_.

Now wait a minute or two while your app is in the oven. You can follow what's happening in the logs. See the buttons in the bottom right corner.

While we are waiting, what do you think is happening under the hood?

<details>
  <summary markdown='span'><strong> 💡 Answer </strong></summary>

  Something you already know.

  Streamlit Community Cloud:
  - Checks out the contents of your repo (only the branch you selected in the settings).
  - Builds a Docker image with your dependencies in the `uv.lock`, and your code (both from the repo).
  - Runs a container with that image, starting `streamlit run` in the `CMD`.

</details>

By now your app should be up and running? Is it functioning?

Probably not. Try to understand the error message and find out what's wrong.

<details>
  <summary markdown='span'><strong> 💡 Answer </strong></summary>

  The app still connects to `https://localhost:8000`, but that only works locally. To have the app working in the cloud, it needs to connect to the API in the cloud!

</details>

## 4) Fix the problem in a robust way

The quick and dirty way to fix this is to change the URL inside the code. But that is not very robust:
- Changing the code every time just to change the address of the URL is ugly.
- We'd also have to remember every time to switch to the cloud URL when deploying.
- We prefer to have one version of the code that works both locally and in when deployed.

Let's do this the proper way with Streamlit built-in _[secrets](https://docs.streamlit.io/develop/concepts/connections/secrets-management)_ functionality.

Secrets are typically used to store sensitive credentials like usernames and passwords instead of including them directly in the code base (**never** do that!).

You can also use them to store the URL of our API. The handy thing is that you can use two sets of secrets:
- One local set on our machine, with the URL of our local API, or the cloud one, you can choose and switch easily by changing the secret.
- One on Streamlit Community Cloud, with the cloud URL.

They will work a bit like environment variables with `.env`:
- You will define the secrets (variables) in a configuration file.
- You will be able to use them in your code.

This is an example of *separating configuration from code*: setting the API address to use, usernames, passwords, etc. should be made in configuration files, so we don't have to change the (Python) code to switch to another API for example.

Let's do this!

### 4.1) Local secrets

👉 To store and use local secrets:

1. Create a new directory `.streamlit` (the dot at the front is important!).
1. Inside `.streamlit`, create a new file `secrets.toml`.
1. Inside that file, write `API_URL = "http://localhost:8000"`.

👉 Make sure to add `secrets.toml` to your `.gitignore` so you don't accidentally commit your secrets!

Why `.toml`? We have already seen that (`pyproject.toml`). TOML, or _Tom’s Obvious, Minimal Language_ is a simple, human-readable configuration format. It uses a clear key–value structure.

### 4.2) Use the secret in the app

These secrets are very easy to use in our code.

It works similar to using environment variables in code. It's as easy as accessing a value from a dict. (See the challenge _Environment Variables_ in the _Python for Data Science_ unit.)

- Using environment variables: `os.environ['SOME_ENV_VARIABLE']`.

- Using Streamlit secrets: `st.secrets['SOME_SECRET']`.

👉 Let's change the code:

1. Starting from `master`, create a new branch `url-via-secrets`.
1. Open `app.py`.
1. Change the line where you defined the URL, and change it to use the secret you defined in the `secrets.toml`.
1. Run the app, and check if it still works.
1. Keep the app running.
1. Change the `secrets.toml` file to point to your API in the cloud.
1. Reload the app. Does it still work?

Once everything works, commit your changes.

### 4.3 Cloud secrets

In the previous step you excluded the secrets file from our repository. So you can't push it to GitHub. You don't want to either: you don't want to share secrets, right?

Then how do you use the secrets on the cloud?

👉 Easy, in the settings of your app on Streamlit Community Cloud.

1. Go to `https://share.streamlit.io`.
1. Find your list of apps.
1. Click on the three dots next to your app.
1. Choose _Settings_.
1. To the left, choose _Secrets_.
1. Copy the content of your `secrets.toml` (with the cloud url) into the text field.
1. _Save changes_.

Your settings are ready. Now how do you update the code on Streamlit Community Cloud to use the secret?

❓ **How to update your app ?**

Your GitHub repository is the source for the app: each time you push an update to the `master/main` branch of your repo you will see it in the app in almost real time.

👉 Try it out!

1. Go to your terminal, and merge the changes you made into your `master` branch.
1. Push the `master` branch.
1. Go to Streamlit Community Cloud, and see how it is spinning up your app again.
1. Once it's done, check that it works.

That's it, your website is online ! 🚀

Feel free to explore all the possibilities of Streamlit and enhance your app !
➡️ Take a look at the [documentation](https://docs.streamlit.io/)


## 5) Final notes

**If you want to make another app (for example for your project)**

Streamlit Cloud supports unlimited public repos, but only **one private repo**. So if you want to make a second one, one of your two apps will have to be public, or you have to delete the first one.

**Streamlit Community Cloud only works with lightweight apps**

It's a free service after all.

Luckily most of your apps will be lightweight, because you split between a front-end and a back-end. The heavy lifting happens in the back-end where the models are making predictions. The front-end only needs to take a user's input, send it to the back-end and wait for the response.

This is one of the reasons we use separate projects, repositories, and virtual environments for both: we don't want to include heavy data science libraries in our lightweight front-end.


## 6) Run the tests

👉 Go back to the terminal window where you opened this challenge. If you closed it, open a new terminal (outside VS Code), and run the first line from the terminal instructions at the top of this challenge.

👉 Then run the tests for this part:

```bash
pytest
```

If all tests passed (you get a green result), it's time to send your accomplishments to Kitt.

👉 Run the commands below.

```bash
make test
git add tests/test_output.txt
git commit -m "Streamlit deployed with secrets"
git push origin master
```

At this point, your status on Kitt should be green. If not, check with a TA.


## 🏁 Wrapping it up

You have deployed the Streamlit app. You used Streamlit Community Cloud for that. Under the hood that goes through the whole process of building a Docker image, and running container(s) based on that image. The nice touch is that it *abstracts* all of that away: you just push or merge to a branch on the repo. (This is an example of *Continous Deployment*.)

For more advanced use cases, you could take everything into your own hands, and deploy the streamlit app using Docker. Because the bulk of our machinery happens in a back-end API, we usually don't have to do this: we can keep our front-end light.

Finally, you used Streamlit *secrets* to set configuration parameters. That allowed you to *separate code from configuration*. To use another API, you don't need to touch the Python code, you just change a configuration file. This makes everything more robust.


🏁 Congratulations! You have deployed your Streamlit site to the cloud, and made it accessible by the outside world.
