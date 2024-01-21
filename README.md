# Internship Assignment
## Date: 21 Jan 2024

## How to Run
1. Open the terminal and navigate to the project folder.
2. Run the following command:
```
sudo docker-compose build
sudo docker-compose up
```
3. Make sure you have docker installed on your system.

## Endpoints

### 1. /translate
#### Request
```
curl --location --request POST 'http://localhost:5000/translate' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "Hello World",
    "username": "example",
    "password": "password
}'
```
#### Response
```
{
    "translated_text": "Bonjour le monde",
}
```

### 2. /history/example?password=password
#### Request
```
curl --location --request GET 'http://localhost:5000/history/example?password=password'
```
#### Response
```
{
  "translation_history": [
    {
      "original_text": "I am fine",
      "translated_text": "Mir geht's gut."
    },
    {
      "original_text": "Hello",
      "translated_text": "Guten Tag."
    }
  ]
}
```
