---
description: 핀의 정보를 수정하고 불러옵니다.
---

# Pin Page

{% api-method method="get" host="https://localhost:8000" path="/pin" %}
{% api-method-summary %}
Get All Pins
{% endapi-method-summary %}

{% api-method-description %}
현재 존재하는 모든 핀을 불러옵니다.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Pins successfully retrieved.
{% endapi-method-response-example-description %}

```javascript
[
    {
        "name": "first pin's name",
        "img_url": "first pin's img",
        "description": "first pin's description",
        "board": "first pin's board"
    },
    {
        "name": "second pin's name",
        "img_url": "second pin's img",
        "description": "second pin's description",
        "board": "second pin's board"
    }
]
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=404 %}
{% api-method-response-example-description %}
Could not find any pins.
{% endapi-method-response-example-description %}

```javascript
{
    "message": "There's no pin in here."
}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="post" host="https://localhost:8000" path="/pin" %}
{% api-method-summary %}
Create Multiple Pins
{% endapi-method-summary %}

{% api-method-description %}
여러 개의 핀을 동시에 등록합니다.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="Pins" type="array" required=true %}
array of pin data which contains name, img\_url, description, board.
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=201 %}
{% api-method-response-example-description %}

{% endapi-method-response-example-description %}

```
[
    {
        "message": "pin created successfully"
    },
    {
        "message": "pin created successfully"
    }
]
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=400 %}
{% api-method-response-example-description %}

{% endapi-method-response-example-description %}

```
[
    {
        "Exception": "This name already exists in our list"
    },
    {
        "Exception": "This name already exists in our list"
    }
]
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="patch" host="https://localhost:8000" path="/pin/<name>" %}
{% api-method-summary %}
Update Pin with Name
{% endapi-method-summary %}

{% api-method-description %}

{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-body-parameters %}
{% api-method-parameter name="name" type="string" required=true %}
pin's name
{% endapi-method-parameter %}

{% api-method-parameter name="img\_url" type="string" required=true %}
url that connected with pin's img
{% endapi-method-parameter %}

{% api-method-parameter name="description" type="string" required=true %}
pin's description
{% endapi-method-parameter %}

{% api-method-parameter name="board" type="string" required=true %}
board that you want to include your pin
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Pin successfully created.
{% endapi-method-response-example-description %}

```
{
    "name": "Pin's name",
    "img_url": "Pin's img url",
    "description": "Pin's description",
    "board": "Pin's board"
}
```
{% endapi-method-response-example %}

{% api-method-response-example httpCode=400 %}
{% api-method-response-example-description %}

{% endapi-method-response-example-description %}

```

```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="get" host="https://localhost:8000" path="/pin/<name>" %}
{% api-method-summary %}

{% endapi-method-summary %}

{% api-method-description %}

{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-path-parameters %}
{% api-method-parameter name="" type="string" required=false %}

{% endapi-method-parameter %}
{% endapi-method-path-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Pin successfully searched.
{% endapi-method-response-example-description %}

```

```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% api-method method="get" host="https://localhost:8000" path="/pin/<name>" %}
{% api-method-summary %}

{% endapi-method-summary %}

{% api-method-description %}

{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-path-parameters %}
{% api-method-parameter name="" type="string" required=false %}

{% endapi-method-parameter %}
{% endapi-method-path-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Pin successfully searched.
{% endapi-method-response-example-description %}

```

```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

