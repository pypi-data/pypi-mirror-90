<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">PyGoChook</h3>

  <p align="center">
    A simple Python wrapper to send message to Google Chats.
    <br />
    <a href="https://github.com/Lars147/pygochook"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Lars147/pygochook">View Demo</a>
    ·
    <a href="https://github.com/Lars147/pygochook/issues">Report Bug</a>
    ·
    <a href="https://github.com/Lars147/pygochook/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

**Py**thon **Go**ogle **Ch**at Webh**ook** is a simple Python wrapper to send messages to **Google Chat** via their *Incoming Webhooks* (https://developers.google.com/hangouts/chat/how-tos/webhooks).
As for now Google Chat is only available for **G Suite Customers**.

<!-- GETTING STARTED -->
## Getting Started

### Requirements
The package depends on the following packages:
- [aiohttp](https://github.com/aio-libs/aiohttp)

### Installation

Install the package via pip
   ```sh
   pip install pygochook
   ```

<!-- USAGE EXAMPLES -->
## Usage

Send a message to a Google Chat...

```pycon
>>> import pygochook
>>> message = "This is awesome!"
>>> gchat_webhook_url = "https://chat.googleapis.com/..."
>>> gchat_msg_sender = pygochook.MsgSender(message, gchat_webhook_url)
>>> gchat_msg_sender.send()
[{...}]     # response message from google chat
```

Or send a message to multiple Google Chats...

```pycon
>>> import pygochook
>>> message = "This is awesome! I can send even to multiple chats!"
>>> gchat_webhook_urls = ["https://chat.googleapis.com/...", "https://chat.googleapis.com/..."]
>>> gchat_msg_sender = pygochook.MsgSender(message, gchat_webhook_urls)
>>> gchat_msg_sender.send()
[{...}, {...}]     # response message from google chat
```

With the use of `aiohttp` the requests will be performed asynchronously. Hence, it does not matter if you send the message to one or multiple Google Chats with respect to response time. An example:

```pycon
>>> import pygochook
>>> @timer
... def to_one_chat(msg, url):
...     gchat_sender = pygochook.MsgSender(msg, url)
...     return gchat_sender.send()
... 
>>> @timer
... def to_multi_chats(msg, urls):
...     gchat_sender = pygochook.MsgSender(msg, urls)
...     return gchat_sender.send()
... 
>>> message = "Time does not even matter!"
>>> url = "https://chat.googleapis.com/..."
>>> urls = ["https://chat.googleapis.com/...", ..., "https://chat.googleapis.com/..."]  # 10 Chat API-URLs
>>>
>>> to_one_chat(message, url)   # send to one chat
Total execution time: 454 ms
>>>
>>> to_multi_chat(message, url)   # send to 10 chats
Total execution time: 2007 ms
```

Because of the asynchronous structure, the total function execution time is as long as the longest response time.


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Lars147/pygochook/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Lars147/pygochook](https://github.com/Lars147/pygochook)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Best README Template](https://github.com/othneildrew/Best-README-Template)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Lars147/pygochook.svg?style=for-the-badge
[contributors-url]: https://github.com/Lars147/pygochook/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Lars147/pygochook.svg?style=for-the-badge
[forks-url]: https://github.com/Lars147/pygochook/network/members
[stars-shield]: https://img.shields.io/github/stars/Lars147/pygochook.svg?style=for-the-badge
[stars-url]: https://github.com/Lars147/pygochook/stargazers
[issues-shield]: https://img.shields.io/github/issues/Lars147/pygochook.svg?style=for-the-badge
[issues-url]: https://github.com/Lars147/pygochook/issues
[license-shield]: https://img.shields.io/github/license/Lars147/pygochook.svg?style=for-the-badge
[license-url]: https://github.com/Lars147/pygochook/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
<!-- [linkedin-url]: https://linkedin.com/in/Lars147 -->