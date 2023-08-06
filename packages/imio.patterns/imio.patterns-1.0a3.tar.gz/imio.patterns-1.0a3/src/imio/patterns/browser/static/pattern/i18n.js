/* i18n integration.
 *
 * This is a singleton.
 * Configuration is done on the body tag data-i18ncatalogurl attribute
 *     <body data-i18ncatalogurl="/plonejsi18n">
 *
 *  Or, it'll default to "/plonejsi18n"
 */

define([
  'mockup-i18n'
], function(I18N) {
  'use strict';

  // we're creating a singleton here so we can potentially
  // delay the initialization of the translate catalog
  // until after the dom is available
  var _t = null;
  if (_t === null) {
    var i18n = new I18N();
    var domain = 'imio.patterns';
    i18n.loadCatalog(domain);
  }
  return function(msgid, keywords) {
    if (_t === null) {
      _t = i18n.MessageFactory(domain);
    }
    return _t(msgid, keywords);
  };
});
