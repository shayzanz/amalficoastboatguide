// www.amalficoastboatguide.com -> amalficoastboatguide.com (301), everything else from ./site
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'www.amalficoastboatguide.com') {
      url.hostname = 'amalficoastboatguide.com';
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
