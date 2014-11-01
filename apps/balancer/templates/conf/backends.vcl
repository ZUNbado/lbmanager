{% for backend in backends %}
backend {{ backend.name }} {
	.host = "{{ backend.address }}";
}
{% endfor %}

{% for director in directors %}
director {{ director.name }} {{ director.dirtype }} {
   {% for back in director.backends.all %}
   {
      .backend = "{{ back.name }}";
   }
   {% endfor %}
}
{% endfor %}
