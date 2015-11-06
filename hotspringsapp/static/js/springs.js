/*
 * For utility functions, included by all pages.
 */


function getChemUnits(displayName) {
   if (['methane', 'carbon monoxide', 'hydrogen'].indexOf(displayName.toLowerCase()) >= 0) {
	  return '\u03BCM';
   }
   
   return 'ppm';
}