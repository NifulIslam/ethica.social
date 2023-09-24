# Ethica.social - A Social Media Platform Focused on Mental Health and Data Privacy

## About Ethica.social

Ethica.social is a social media platform designed with a strong focus on mental health and data privacy. Our platform offers a range of unique features aimed at ensuring a healthier and more secure social media experience for users. Unlike many other social media platforms, Ethica.social does not rely on advertising, guaranteeing user data privacy.

## Key Features

| ![Customized Reaction](https://github.com/NifulIslam/ethica.social/blob/main/Screenshots/Screenshot_20220923_214846.png) *Customized Reaction* | ![Messenger](https://github.com/NifulIslam/ethica.social/blob/main/Screenshots/Screenshot_20220923_215040.png) *Messenger Feature* |
| :---: | :---: |
| **AI-based Post Recommendation:** Our intelligent recommendation system helps you discover relevant content tailored to your interests. | **Maximum Post View Limit:** Set limits on how often you view posts to avoid overconsumption. |
| **Messaging Functionality:** Stay connected with your friends through our built-in messenger. | **Post Translation:** Translate posts into your preferred language for seamless communication. |
| **Email-based Password Recovery:** Securely recover your account with email verification. | **Customized Reactions:** Express your emotions with unique reaction options. |
| **Cover Photo and Profile Photo Updates:** Personalize your profile with custom images. | **User Following and Donation:** Connect with others and support causes you care about. |
| **Anonymous Data Purchasing (in JSON format):** Buy and use data without compromising your identity. | **Opportunity to Earn Money:** Choose to sell your data for extra income (optional). |
| **Blood Donation Platform:** Find and organize blood donation events within the community. | **Advanced Search Functionality:** Search by name, location, post content, and more. |
| **Various Other Small Features:** Enhance your social media experience with additional functionalities. |  |

## Technologies Used

- Django
- MongoDB Atlas (cloud)
- HTML
- CSS
- JavaScript
- jQuery

## Installation

To set up Ethica.social locally, follow these steps:

1. Install the required Python packages with the following commands:

```bash
pip install django pymongo pymongo[srv] requests googletrans==3.1.0a0 spacy nltk opencv-python
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
