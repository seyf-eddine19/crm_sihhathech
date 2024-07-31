// document.addEventListener('DOMContentLoaded', function() {
//     const typeAbonnementSelect = document.getElementById('id_type_abonnement');
//     const versionOffreSelect = document.getElementById('id_version_offre');

//     function filterVersions() {
//         const typeAbonnementId = typeAbonnementSelect.value;
//         let firstOptionValue = '';

//         // Iterate through options to filter and track the first valid option
//         for (const option of versionOffreSelect.options) {
//             if (option.dataset.abonnementTypeId === typeAbonnementId || option.value === '') {
//                 option.style.display = 'block';
//                 if (!firstOptionValue && option.value) {
//                     firstOptionValue = option.value;
//                 }
//             } else {
//                 option.style.display = 'none';
//             }
//         }

//         // Set the first valid option as selected
//         if (firstOptionValue) {
//             versionOffreSelect.value = firstOptionValue;
//         } else {
//             versionOffreSelect.value = ''; // Clear selection if no valid option
//         }
//     }

//     typeAbonnementSelect.addEventListener('change', filterVersions);
//     filterVersions(); // Initial call to filter versions on page load
// });
