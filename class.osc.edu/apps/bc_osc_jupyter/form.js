'use strict'


const account_lookup = {
  "ASTRONOMY8824_OSU": "PAS2055",
  "BIOCHEM5721":   "PAS1745",
  "BMI5780_OSU":   "PAS2048",
  "PHYSICS6820":   "PAS1759",
  //OSCJUPYTER entry not required
  "PHYS280_WIT":   "PWIT0412",
  "PHYS4032_OU":   "PHS0346",
  "PHYS5071_OU":   "PHS0353",
  "PHYS4025_UC":   "PES0840",
  "PHYSICS5680_OSU": "PAS2038",
  "MATH2530_OU":   "PHS0352",
  "MPA5830_OU":    "PHS0354",
  "GRADTDA5622":   "PAS1871",
  "CSE519401":     "PAS1911",
  "CSCI6950_YSU":  "PLS0150",
  "EEOB889619":    "PAS1918",
  "GRADTDA5620":   "PAS1979",
  "MIME4980":      "PJS0333",
  "2021CCCBISR":   "PAS1984",
}

const k8s_classrooms = [
  { 'name': 'GRADTDA5620' },
  { 'name': 'MPA5830_OU' },
  {
    'name': 'PHYSICS5680_OSU',
    'cores': 4,
  },
  {
    'name': 'ASTRONOMY8824_OSU',
    'node_type': 'pitzer'
  },
  {
    'name': 'PHYS4025_UC',
    'node_type': 'pitzer'
  },
  {
    'name': 'CSCI6950_YSU',
    'node_type': 'pitzer',
    'cores': 2,
  },
  {
    'name': 'MIME4980',
    'node_type': 'pitzer'
  },
  {
    'name': 'BMI5780_OSU',
    'node_type': 'pitzer'
  },
];

var staff = false;

/**
 * Add a change listener to the version select
 */
function set_version_change_handler() {
  const version_select = $("#batch_connect_session_context_version");

  version_select.change(function(event){
    change_account(event);
    show_cores(event);
    set_cluster(event);
  });
}

/**
 * Change the account form value given a change from in version.
 * 
 * @param  {Object} event The change event
 */
function change_account(event){
  if(staff) {
    return;
  }

  for(var cls in account_lookup){
    var found = RegExp(cls).test(event.target.value);

    if(found){
      const account = $('#batch_connect_session_context_account');
      account.val(account_lookup[cls]).change();
    }
  }
}

/**
 * Show the cores element if the event changes the classroom to
 * allowed classrooms.
 *
 * @param  {Object} event The change event
 */
function show_cores(event){
  if(staff) {
    return;
  }

  const show = /PHYSICS6820/.test(event.target.value);
  toggle_visibility_of_form_group('#batch_connect_session_context_num_cores', show);

  // default to 1 core
  if(!show){
    const cores = $('#batch_connect_session_context_num_cores');
    cores.val("1");
  }
}

/**
 * Toggle the visibility of a form group
 *
 * @param      {string}    form_id  The form identifier
 * @param      {boolean}   show     Whether to show or hide
 */
function toggle_visibility_of_form_group(form_id, show) {
  let form_element = $(form_id);
  let parent = form_element;

  // kick out if you can't find the element
  if(parent.size() <= 0){
    return;
  }

  while (
    (! parent[0].classList.contains('form-group')) &&
    (! parent.is('html')) // ensure that we don't loop infinitely
  ) {
    parent = parent.parent();
  }

  // If parent is HTML then something has gone wrong and visibility should not be changed
  if ( parent.is('html') ) {
    return;
  }

  if(show) {
    parent.show();
  } else {
    parent.hide();
  }
}

/**
 * Set the staff variable given what's in the form
 */
function set_staff() {
  const staff_ele = $('#batch_connect_session_context_staff');

  if(staff_ele.val() == "1") {
    staff = true;
  }
}

/**
 * Alert users if they're launching a regular version of this
 * app with no extra classroom materials,
 */
function alert_if_one_version(one_version) {
  if(one_version) {
    alert('You are not a part of any classroom project. The Jupyter launched here will not include classroom materials.');
  }
}

function set_cluster(event) {
  var node_type = 'any';
  var cluster = 'owens';
  var num_hours_max = undefined;
  var cores = 1;

  k8s_classrooms.forEach(cls => {
    var k8s = RegExp(cls['name']).test(event.target.value);

    if(k8s) {
      node_type = cls['node_type'] || 'owens';
      cores = cls['cores'] || cores;
      cluster = k8s_cluster();
      num_hours_max = cls['max_walltime'] || 2;
    }
  });

  $('#batch_connect_session_context_cluster').val(cluster).change();
  $('#batch_connect_session_context_node_type').val(node_type).change();
  $('#batch_connect_session_context_num_cores').val(cores).change();

  if(num_hours_max !== undefined) {
    $('#batch_connect_session_context_bc_num_hours').attr({'max': num_hours_max});
  } else {
    $('#batch_connect_session_context_bc_num_hours').removeAttr('max');
  }
}

function k8s_cluster() {
  const hostRex = /\w+(-dev|-test){0,1}.osc.edu/;
  const match = hostRex.exec(window.location.hostname);

  if(match.length >= 2 && match[1] !== undefined) {
    return `kubernetes${match[1]}`;
  } else {
    return 'kubernetes';
  }
}

set_staff();

var one_version = $('#batch_connect_session_context_version').length == 0;
var show_account =  one_version || staff;

alert_if_one_version(one_version);
set_version_change_handler();
toggle_visibility_of_form_group('#batch_connect_session_context_account', show_account);
toggle_visibility_of_form_group('#batch_connect_session_context_staff', false);
toggle_visibility_of_form_group('#batch_connect_session_context_node_type', false);

// Fake some events to initialize things
change_account({ target: document.querySelector('#batch_connect_session_context_version') });
show_cores({ target: document.querySelector('#batch_connect_session_context_version') });
set_cluster({ target: document.querySelector('#batch_connect_session_context_version') });
