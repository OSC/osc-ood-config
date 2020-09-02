'use strict'


const account_lookup = {
  "STAT2480":      "PAS1758",
  "STAT3202":      "PAS1644",
  "STAT5730":      "PAS1642",
  "ANTHROP9982":   "PAS1723",
  "TDAI":          "PAS1732",
  "OSCWORKSHOP":   "PZS0687",
  "OSCRNASEQ":     "PZS1010",
  "PUBHLTH5015":   "PAS1754",
  "BANA7025_UC":   "PES0835",
  "RWORKSHOP_UC":  "PES0836",
  "BANA4090_UC":   "PES0834",
}

var staff = false;

/**
 * Add a change listener to the version select
 */
function set_version_change_hander() {
  const version_select = $("#batch_connect_session_context_version");

  version_select.change(function(event){
    change_project(event);
    show_cores(event);
  });
}

/**
 * Change a project form value given a change from in version.
 * 
 * @param  {Object} event The change event
 */
function change_project(event){
  if(staff) {
    return;
  }

  for(var cls in account_lookup){
    var found = RegExp(cls).test(event.target.value);

    if(found){
      const project = $('#batch_connect_session_context_project');
      project.val(account_lookup[cls]);
    }
  }
}

function show_cores(event){
  if(staff) {
    return;
  }

  const show = /ANTHROP9982|OSCWORKSHOP/.test(event.target.value);
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

set_staff();

set_version_change_hander();
toggle_visibility_of_form_group('#batch_connect_session_context_project', staff);
toggle_visibility_of_form_group('#batch_connect_session_context_staff', false);

// Fake some events to initialize things
change_project({ target: document.querySelector('#batch_connect_session_context_version') });
show_cores({ target: document.querySelector('#batch_connect_session_context_version') });
