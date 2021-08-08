// ============ Various tooltips ===============
tippy('#tip-visib', {
	content: 'Change the visibility of your collection, set it to public or private.',
});
tippy('#tip-lock', {
	content: 'Set the password for your collection.',
});

tippy('#tip-copyn', {
	content: 'Copy the link of this collection.',
});

tippy('#tip-desc', {
	content: 'View the description.',
});

tippy('#tip-add', {
	content: 'Create a new collection.',
});

tippy('#tip-share', {
	content: 'Share this collection with others.',
});

tippy('#tip-addlink', {
	content: 'Add a new link to this collection.',
});

// ================== Cookie to add it to Fetch request =============
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

document.querySelector("#pop-x").onclick = () => {
	document.querySelector("#popup").style.display = 'none';
}

// ============ Toast functions ==================
function toast(text) {
	var x = document.getElementById("toast");
	document.getElementById("desc").innerHTML = text;
	x.className = "show";
	setTimeout(function () {
		x.className = x.className.replace("show", "");
	}, 5000);
}

function base_copy(text, typ) {
	var dn = document.createElement("textarea");
	document.body.appendChild(dn);
	dn.value = text;
	dn.select();
	document.execCommand("copy");
	document.body.removeChild(dn);
	toast(typ + " successfully copied ✔");
}

function copydesc() {
	base_copy(text, "Unilection description")
}

function copylink() {
	var text = window.location.href;
	base_copy(text, "Link")
}

// =========== Updating the sort that is newest or oldest =============
function update_sort(val) {
	var url = new URL(location.href)
	url.searchParams.set('sort', val);
	var modifiedUrl = url.toString();
	window.location.href = modifiedUrl;
}

// ===========   Functions for various popups alerts  ===========
function setup_popup(data) {
	document.querySelector("#password").style.display = "none";
	document.querySelector("#third__").style.display = "none";
	document.querySelector("#tabtn").textContent = data.getAttribute("description");

	document.querySelector("#card_link").onclick = () => {
		var element = document.createElement("input");
		document.querySelector("body").appendChild(element);
		element.value = data.getAttribute("url");
		element.select();
		document.execCommand("copy");
		element.remove();
		toast("Link successfully copied ✔");
	};

	document.querySelector("#popup").style.display = "block";
}

function setup_popup_dsc(data) {
	document.querySelector("#password").style.display = "none";
	document.querySelector("#tabtn").textContent = data.getAttribute("description");
	document.querySelector("#third__").style.display = "none";
	document.querySelector("#popup").style.display = "block";
}

function share() {
	document.querySelector("#password").style.display = "none";
	document.querySelector("#tabtn").innerHTML = window.location.origin + "<br> <br>" + "Consider sharing with your friends!";
	base_copy(window.location.href, "Link")
	document.querySelector("#third__").style.display = "none";
	document.querySelector("#popup").style.display = "block";
}


function setup_pp() {
	document.querySelector("#password").style.display = "block";
	document.querySelector("#tabtn").textContent = "Remember you can set the password only once.";
	document.querySelector("#third__").style.display = "none";
	document.querySelector("#popup").style.display = "block";
}

function close_alertp() {
	document.querySelector("#alertp").style.display = "none";
}