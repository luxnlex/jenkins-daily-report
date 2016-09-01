jQuery(document).ready(function ($) {
			function l_tooltip(target_items, name) {
				$(target_items).each(function (i) {        
					$("body").append("<div class='" + name + "' id='" + name + i + "'><p>" + $(this).attr('title') + "</p></div>");        
					var tooltip = $("#" + name + i);        
					if ($(this).attr("title") != "" && $(this).attr("title") != "undefined") {        
						$(this).removeAttr("title").mouseover(function () {                
							tooltip.css({
								opacity: 0.9,
								display: "none"
							}).fadeIn(500);        
						}).mousemove(function (kmouse) {                
							tooltip.css({
								left: kmouse.pageX + 15,
								top: kmouse.pageY + 15,
							});        
						}).mouseout(function () {                
							tooltip.fadeOut(10);        
						});        
					}    
				});
			}
			l_tooltip(".ttp_lnk a","tooltip");
		});