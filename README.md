<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



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
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
  <h3 align="center">Time Series Forecasting</h3>
  <p align="center">
    Using Open Remote time series data to predict the future!
    <br />
    <a href="https://github.com/StephenFierce/TimeSeriesForecasting/wiki"><strong>Explore the wiki »</strong></a>
    <br />
    <br />
    <a href="https://github.com/StephenFierce/TimeSeriesForecasting/issues">Report Bug</a>
    ·
    <a href="https://github.com/StephenFierce/TimeSeriesForecasting/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#communicator">Communicator</a></li>
        <li><a href="#generic-forecasting">Generic Forecasting</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Introduction on project

![C4 Component Diagram](https://github.com/StephenFierce/TimeSeriesForecasting/blob/master/blob/C4%20Component%20Diagram.png)

### Communicator


### Generic Forecasting


Use the <a href="#getting-started">Getting Started</a> to get started.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [Next.js](https://nextjs.org/)
* [React.js](https://reactjs.org/)
* [Vue.js](https://vuejs.org/)
* [Angular](https://angular.io/)
* [Svelte](https://svelte.dev/)
* [Laravel](https://laravel.com)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This guide contains instructions on setting up the Time Series Forecasting project locally.
To get a local copy up and running follow these steps.


### Prerequisites

* python 3.9.12
* Tensorflow
* Docker Desktop
* Java IDE (IntelliJ)
* Open Remote Dev Environment

_Before starting to setup the Time Series Forecasting project it is required to setup an Open Remote Dev Environment._


#### Open Remote Dev Environment
1. Setup an OR dev enviornment using the dev-testing.yml profile: [Open Remote Developer Guide](https://github.com/openremote/openremote/wiki/Developer-Guide%3A-Setting-up-an-IDE)

2. Create an asset and attribute using [Create an asset and attribute](https://github.com/StephenFierce/TimeSeriesForecasting/wiki/Creating-an-asset-and-attribute).

3. Create an MQTT user using [Create a MQTT user](https://github.com/StephenFierce/TimeSeriesForecasting/wiki/Creating-a-MQTT-user).

_This concludes the Open Remote Dev Environment setup. Up next is the installation and configuration of the Time Series Forecasting project._



### Installation

_This is the installation and configuration guide for the Time Series Forecasting project._

1. Clone the repo
   ```sh
   git clone https://github.com/StephenFierce/TimeSeriesForecasting.git
   ```
#### Configure the Communicator
2. Open `main.py` 
3. Paste the `Asset ID` from the [Create an asset and attribute](https://github.com/StephenFierce/TimeSeriesForecasting/wiki/Creating-an-asset-and-attribute) guide into the `assetID` variable.
4. Paste the `MQTT user secret` from the [Create a MQTT user](https://github.com/StephenFierce/TimeSeriesForecasting/wiki/Creating-a-MQTT-user) guide into the `password` variable.
5. Change `IP_ADDRESS` your current local IP

#### Build Docker Images
6. Build the Communicator image
> Make sure the terminal location is in the `TimeSeriesForecasting` directory.
   ```sh
   docker build -t communicator .
   ```
7. Build the Generic Forecasting image
> Make sure the terminal location is in the `TimeSeriesForecasting/flask_api` directory.
   ```sh
   docker build -t time_series_api .
   ```
   
#### Run Docker Images
8. Run the Communicator image
   ```sh
   docker run --rm --net=host communicator
   ```

9. Run the Generic Forecasting image
   ```sh
   docker run --rm -p 5096:5096 time_series_api
   ```
   
> --rm removes the image after exiting, this prevents the build up of images during development.

Result:
![MQTT Connected Screen Shot](https://github.com/StephenFierce/TimeSeriesForecasting/blob/master/blob/MQTT_Connected.png)

10. Test the installation by changing the `power` attribute value on the asset page of the Open Remote manager.

Result:
![Prediction Log Screen Shot](https://github.com/StephenFierce/TimeSeriesForecasting/blob/master/blob/Prediction_Log.png)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Stephen Fiers - [@theguanyin](https://twitter.com/TheGuanyin)

Project Link: [Time Series Forecasting](https://github.com/StephenFierce/TimeSeriesForecasting)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/StephenFierce/TimeSeriesForecasting.svg?style=for-the-badge
[contributors-url]: https://github.com/StephenFierce/TimeSeriesForecasting/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/StephenFierce/TimeSeriesForecasting.svg?style=for-the-badge
[forks-url]: https://github.com/StephenFierce/TimeSeriesForecasting/network/members
[stars-shield]: https://img.shields.io/github/stars/StephenFierce/TimeSeriesForecasting.svg?style=for-the-badge
[stars-url]: https://github.com/StephenFierce/TimeSeriesForecasting/stargazers
[issues-shield]: https://img.shields.io/github/issues/StephenFierce/TimeSeriesForecasting.svg?style=for-the-badge
[issues-url]: https://github.com/StephenFierce/TimeSeriesForecasting/issues
[license-shield]: https://img.shields.io/github/license/StephenFierce/TimeSeriesForecasting.svg?style=for-the-badge
[license-url]: https://github.com/StephenFierce/TimeSeriesForecasting/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
