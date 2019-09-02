# Pin Page

{% api-method method="get" host="https://localhost:8000" path="/pin/<name>" %}
{% api-method-summary %}
Get Pin with Name
{% endapi-method-summary %}

{% api-method-description %}
This endpoint allows you to get free cakes.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Pin successfully searched.
{% endapi-method-response-example-description %}

```javascript
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
Could not find pin matching this query.
{% endapi-method-response-example-description %}

```javascript
{
    "message": "Given name does not exist in our Pin name list"
}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}



