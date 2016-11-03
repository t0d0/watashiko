$.extend({
	"put" : function (url, data, success, error) {
		error = error || function() {}; 
		return $.ajax({
			"url" : url,
			"data" : data,
			"success" : success,
			"type" : "PUT",
			"cache" : false,
			"error" : error,
			"dataType" : "json"
		});
	},
	"del" : function (url, data, success, error) { 
		error = error || function() {};
		return $.ajax({
			"url" : url,
			"data" : data,
			"success" : success,
			"type" : "DELETE",
			"cache" : false,
			"error" : error,
			"dataType" : "json"
		});
	}
});