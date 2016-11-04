$.extend({
	"put" : function (url, data, success, error) {
//		error = error || function() {}; 
		return $.ajax({
			"url" : url,
			"data" : data,
			"complete" : success,
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
			"complete" : success,
			"type" : "DELETE",
			"cache" : false,
			"error" : error,
			"dataType" : "json"
		});
	}
});