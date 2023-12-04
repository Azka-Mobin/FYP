/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'client/templates/client/*.html',
    'core/templates/core/*.html',
    'core/templates/core/partials/*.html',
    'dashboard/templates/dashboard/*.html',
    'lead/templates/lead/*.html',
    'team/templates/team/*.html',
    'userprofile/templates/userprofile/*.html',
    'campaigns/templates/campaigns/*.html',
    'product/templates/product/*.html',
  ],
  theme: {
    extend: {
      backgroundColor: {
        'purple': '#8a2be2',
        'teal': '#008080',
        'black':'#000000',
        'custom-color-1': '#FFA500', // Your custom color
        'custom-color-2': '#00FF00', // Another custom color
        // Add more custom background colors as needed
      },
    },
  },
  plugins: [],
}

