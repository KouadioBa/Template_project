odoo.define("open_livreur_theme.delivery_control", function (require) {
	"use strict";

	// cacher le header et le footer
	if (location.pathname == '/page/job/list') {
		$('.o_affix_enabled').addClass('d-none')
		$('.o_footer').addClass('d-none')
	}

	// actualiser la liste des commandes
	let refresh_cmd_list = function () {
		$.ajax({
			type: "GET",
			url: location.pathname,
			cache: "false",
			success: function (res) {
				if ($('.active-picking').length == 1) {
					let active_pick_id = $('.active-picking input[name=picking]').val()
					$(res).find('.div-each-cmd input[value=' + active_pick_id + ']').each(function () {
						let current_shipp_det = $('.active-picking .shipping-details div')
						let new_shipp_det = $(this).parent('.shipping-details').children("div")
						if (current_shipp_det.find('.timeline').text() != new_shipp_det.find('.timeline').text()) {
							console.log("***** Refresh timeline *****")
							$('.active-picking .shipping-details div').html(new_shipp_det.html())
						}
					})
				}

				$('.order-list').each(function () {
					// actualiser la liste dans chaque tab-panel
					let tabpan_id = $(this).parent('.tab-pane').attr('id')
					let orderlist_selector = '#' + tabpan_id + ' .order-list'
					let current_txt = $(orderlist_selector).text()
					let new_txt = $(res).find(orderlist_selector).text()
					if (current_txt != new_txt) {
						if ($('.active-picking').length == 0) {
							console.log("***** Refresh order list *****")
							$(orderlist_selector).html($(res).find(orderlist_selector).html())
							$('#' + tabpan_id + '-tab').html($(res).find('#' + tabpan_id + '-tab').html())
						}
					}
				});
			}, Error: function (x, e) {
				alert("Some error");
			}
		});
	}

	// requete de l'atat de la commande
	function driver_assignmt_action(picking, action_type) {
		let value = {
			"picking_id": picking,
			"action_type": action_type,
		}
		console.log(value)
		$.ajax({
			url: "/driver-assignment-action",
			data: value,
			cache: "false",
			success: function (res) {
				if (res == 'accepted' || res == 'rejected') {
					$('#assignment-prompt').modal('hide')
				}
			},
			Error: function (x, e) {
				alert("Some error");
			}
		});
	}

	// accepter ou rejeter une commande
	function prompt_assignment_confirmation(text, color) {
		let order_name = $('.active-picking input[name=order_name]').val()
		$(".modal-footer .confirm-action").css('color', color)
		$(".modal-body div").text(text)
		$(".modal-header #order-name").text(order_name)
		$('#assignment-prompt').modal('show')
	}

	$(document).ready(function () {
		if (location.pathname == '/page/job/list') {
			$('.o_affix_enabled').addClass('d-none')
			$('.o_footer').addClass('d-none')
		}

		$('#nav-commandes').on("click", '.recap .nav-item', function (e) {
			if ($(this).hasClass('active')) {
				$('#nav-commandes .recap .nav-item.active').removeClass('active show')
				$('#nav-commandes #pills-tabContent .fade.active').removeClass('active show')
				$('#nav-commandes #pills-tabContent #pills-home').addClass('active show')
				e.preventDefault();
				return false;
			}
		});

		//Refresh
		let refresh_all_time_cmd_list = setInterval(refresh_cmd_list, 3000);
		if (!location.pathname.includes('/page/job/list')) {
			clearInterval(refresh_all_time_cmd_list);
		}

		$('.submit-checkbox button').click(function (e) {
			let checked_box = $('.calendar-day.active.show .time-form-check input:checked')
			let checks_string = ''
			$.each(checked_box, function (index, value) {
				$(value).val()
				checks_string += $(value).val() + ","
			});

			let value = {
				"checked_box": checks_string,
				"driver_id": parseInt($('input[name=driver]').val()),
				'date': $('.calendar-day.active.show input[name=date]').val()
			}

			$.ajax({
				url: "/post/driver/timecheck/",
				data: value,
				cache: "false",

				success: function (res) {
					console.log(res)
					$(".calendar-day.active.show").load(" .calendar-day.active.show > *")
				},
				Error: function (x, e) {
					alert("Some error");
				}
			});
		});

		// Lorsque le client choisi un mode de paiement, enregistrer dans la commande
		$('#o_payment_form_pay').click(function (e) {
			let acquirer_id = parseInt($('.o_payment_form input[name=pm_id]:checked').attr('data-acquirer-id'))
			let order_id = parseInt($('input[name=order_id]').val())

			let value = {
				"order_id": order_id,
				"acquirer_id": acquirer_id,
			}

			$.ajax({
				url: "/payment-method",
				data: value,
				cache: "false",

				success: function (res) {
					alert(res)
				},
				Error: function (x, e) {
					alert("Some error");
				}
			});
		});

		// accept
		$('.order-list').on("click", '#accept_assignment', function () {
			// sectionner la commande
			$(this).parent().parent().parent().addClass("active-picking")
			let text = "Vous avez décidé de prendre cette commande. Êtes vous sur de vouloir effectué cette livraison ?"
			$('#assignment-prompt #accept').attr('checked', 'checked')
			prompt_assignment_confirmation(text, '#28A745')
		});

		// reject
		$('.order-list').on("click", '#reject_assignment', function () {
			// sectionner la commande
			$(this).parent().parent().parent().addClass("active-picking")
			let text = "Voulez-vous vraiment rejeter cette livraison ?"
			$('#assignment-prompt #reject').attr('checked', 'checked')
			prompt_assignment_confirmation(text, "#911224")

		});

		// confirm assignation
		$('#assignment-prompt').on("click", '.confirm-action', function () {
			let picking = parseInt($('.active-picking input[name=picking]').val())
			let action_type = $('#assignment-prompt input:checked').val()
			driver_assignmt_action(picking, action_type)
		});

		$('#assignment-prompt').on("click", '.cancel-action', function () {
			// desectionner la commande
			$('.div-each-cmd').removeClass("active-picking")
			$('#assignment-prompt input:checked').attr('checked', 'checked')
		});

		$('#assignment-prompt').on('hidden.bs.modal', function () {
			// $("#assignment-prompt").on("hidden", function () {
			$('.div-each-cmd').removeClass("active-picking")
			$('#assignment-prompt input:checked').attr('checked', 'checked')
		})

		// order Details
		$('.order-list').on("click", '.order-details', function () {
			let part_lat = $(this).parent().children('input[name=part_lat]').val()
			let part_long = $(this).parent().children('input[name=part_long]').val()
			let order_name = $(this).parent().children('input[name=order_name]').val()
			$('input[name=latitude]').val(part_lat)
			$('input[name=longitude]').val(part_long)
			$('#current-order-name').text(order_name)

			// redimentionner
			$('.dashbd-mdblc').removeClass("d-md-block")
			$('.dashbd-mdflx').removeClass("d-md-flex")
			$('.div-each-cmd').removeClass("p-3")
			$('.div-each-cmd').addClass("col-md-12 p-0")
			$('.cmd-list').removeClass('col')
			$('#pills-tabContent .tab-pane.active').addClass('dbl-height')

			// cacher toutes les commandes
			$('.dashbd-elt').addClass("d-none")
			$('.shipdet-elt').removeClass("d-none")

			// cacher la navbar pour les petits ecrans 
			$('.menu').addClass('none-on-xs-details')

			$(this).parent().parent().parent().find('.shipping-details').removeClass("d-none")
			// sectionner la commande
			$(this).parent().parent().parent().addClass("active-picking")
			// afficher uniquement la concernée
			$(this).parent().parent().parent().removeClass("d-none")
		});

		// back
		$('.cmd-content-head').on("click", '.back', function () {
			$('input[name=latitude]').val('0')
			$('input[name=longitude]').val('0')

			$('#pills-home').css('height', 'fit-content')
			$('.dashbd-mdblc').addClass("d-md-block")
			$('.dashbd-mdflx').addClass("d-md-flex")
			$('.div-each-cmd').addClass("p-3")
			$('.div-each-cmd').removeClass("col-md-12 p-0")
			$('#pills-tabContent .tab-pane.active').removeClass('dbl-height')

			$('.cmd-list').addClass('col')
			$('.shipdet-elt').addClass("d-none")
			$('.shipping-details').addClass("d-none")
			$('.dashbd-elt').removeClass("d-none")

			// desectionner la commande
			$('.div-each-cmd').removeClass("active-picking")
		});

		// appeler le client
		$('.order-list').on('click', '.call-client .fa-phone-alt', function () {
			let client_mobile_number = $(this).parent().parent().find('.client-mobile').text().replace(/\s/g, '');
			window.location.href = 'tel://' + client_mobile_number;

		})

		// etapes de livraison
		$('.order-list').on('click', '.delivery-step-confirmation', function () {
			let step_id = $('.active-picking .timeline .step .active-circle').parent().parent()
			let picking = parseInt($('.active-picking input[name=picking]').val())

			if (step_id.attr('id') == 'accepted') {
				driver_assignmt_action(picking, 'collect')
			}
			else if (step_id.attr('id') == 'collected') {
				driver_assignmt_action(picking, 'deliver')
			}
		});
	});
});
