# Initial page

{% api-method method="get" host="https://HOST:PORT" path="/pin" %}
{% api-method-summary %}
Get Pins
{% endapi-method-summary %}

{% api-method-description %}
This endpoint allows you to get free cakes.
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
    "message": "Ain't no cake like that."
}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}



