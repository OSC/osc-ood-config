'use strict'


const account_lookup = {
  "STAT2480":      "PAS1758",
  "STAT3202":      "PAS1644",
  "STAT5730":      "PAS1642",
  "ANTHROP9982":   "PAS1723",
  "TDAI":          "PAS1882",
  "OSCWORKSHOP":   "PZS1117",
  "OSCRNASEQ":     "PZS1010",
  "PUBHLTH5015":   "PAS1754",
  "BANA7025_UC":   "PES0835",
  "RWORKSHOP_UC":  "PES0836",
  "BANA4090_UC":   "PES0834",
  "CODECLUB":      "PAS1838",
  "SOCIO5650":     "PAS1844",
  "SOC3549_OSU":   "PAS2017",
  "BM7331":        "PAS1877",
  "EEOB4410":      "PAS1879",
  "GRADTDA5402":   "PAS1873",
  "R_DEMO":        "PZS1118",
  "BMI5730":       "PAS1669",
  "BMI8130_OSU":   "PAS2015",
  "EEOB889619":    "PAS1918",
  "BISRRNASEQ":    "PAS1952",
  "GRADTDA5620":   "PAS1979",
  "2021CCCBISR":   "PAS1984",
};

const k8s_classrooms = [
  {
    'name': 'OSCRNASEQ',
    'max_walltime': 5
  },
  { 'name': 'GRADTDA5620' },
  { 'name': 'SOC3549_OSU' },
  { 'name': 'BMI5730' },
  { 'name': 'STAT2480' },
  {
    'name': 'BMI8130_OSU',
    'cores': 4,
    'node_type': 'pitzer',
    'max_walltime': 4
  }
];

var staff = false;

/**
 * Add a change listener to the version select
 */
function set_version_change_hander() {
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

function show_cores(event){
  if(staff) {
    return;
  }

  const show = /ANTHROP9982|OSCWORKSHOP|OSCRNASEQ|BMI8130_OSU/.test(event.target.value);
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
    alert('You are not a part of any classroom project. The RStduio launched here will not include classroom materials.');
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
set_version_change_hander();
toggle_visibility_of_form_group('#batch_connect_session_context_account', show_account);
toggle_visibility_of_form_group('#batch_connect_session_context_staff', false);
toggle_visibility_of_form_group('#batch_connect_session_context_node_type', false);

// Fake some events to initialize things
change_account({ target: document.querySelector('#batch_connect_session_context_version') });
show_cores({ target: document.querySelector('#batch_connect_session_context_version') });
set_cluster({ target: document.querySelector('#batch_connect_session_context_version') });
