import{_ as t,H as s,h as o,l as i,c as n}from"./e.c3fea9f7.js";import{m as e}from"./c.2d2c6ca5.js";import"./c.146c1503.js";import{v as a}from"./c.5cf0c593.js";import"./c.484625a6.js";import"./c.f45da83b.js";let r=t([n("hacs-about-dialog")],(function(t,s){return{F:class extends s{constructor(...s){super(...s),t(this)}},d:[{kind:"method",key:"render",value:function(){return this.active?o`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.narrow?"HACS":"Home Assistant Community Store"}
        hideActions
      >
        <div class="content">
          ${e.html(`\n**${i("dialog_about.integration_version")}:** | ${this.hacs.configuration.version}\n--|--\n**${i("dialog_about.frontend_version")}:** | ${a}\n**${i("common.repositories")}:** | ${this.repositories.length}\n**${i("dialog_about.installed_repositories")}:** | ${this.repositories.filter(t=>t.installed).length}\n\n**${i("dialog_about.useful_links")}:**\n\n- [General documentation](https://hacs.xyz/)\n- [Configuration](https://hacs.xyz/docs/configuration/start)\n- [FAQ](https://hacs.xyz/docs/faq/what)\n- [GitHub](https://github.com/hacs)\n- [Discord](https://discord.gg/apgchf8)\n- [Become a GitHub sponsor? ❤️](https://github.com/sponsors/ludeeus)\n- [BuyMe~~Coffee~~Beer? 🍺🙈](https://buymeacoffee.com/ludeeus)\n\n***\n\n_Everything you find in HACS is **not** tested by Home Assistant, that includes HACS itself._\n_The HACS and Home Assistant teams do not support **anything** you find here._\n        `)}
        </div>
      </hacs-dialog>
    `:o``}}]}}),s);export{r as HacsAboutDialog};
