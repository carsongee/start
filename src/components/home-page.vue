<template>
  <div id="home-page">
    <div class="header">
      <div class="header__links">
        <a
          v-for="link in config.header_links"
          :key="link.url"
          :href="link.url"
          ><img :src="link.img" height="64"/></a>
      </div>
      <h1 class="header__title">{{ config.greeting }} {{ config .name }}</h1>
      <div v-if="config.quote" class="header__quote">
        <p>
          {{ config.quote.quote }} - {{ config.quote.name }}
        </p>
      </div>
    </div>
    <div class="link">
      <input
        class="link__search"
        type="text"
        ref="search"
        v-model="linkSearch"
        placeholder="Search Links"
        @keyup.enter="goToFirstLink"
        @keyup.right="moveFocusRight"
        @keyup.left="moveFocusLeft"
        @keyup.down.prevent="moveFocusDown"
        @keyup.up.prevent="moveFocusUp"
        @focus="resetFocus"
        />
      <transition-group name="bounce" tag="ul" class="link__results">
        <li class="link__result" v-for="link in linkResults" :key="link.url">
          <a
            class="link__link"
            :ref="link.url"
            :href="link.url"
            @keyup.right="moveFocusRight"
            @keyup.left="moveFocusLeft"
            @keyup.down.stop="moveFocusDown"
            @keyup.up.stop="moveFocusUp"
            @keyup.esc="setSearchFocus"
            >
            <span v-if="link.icon !== undefined" :class="link.icon"></span>
            <span class="link__parent" v-if="link.parent">
              {{ link.parent }} &gt;
            </span>
            {{ link.name }}
          </a>
        </li>
      </transition-group>
    </div>
    <git-hub></git-hub>
    <upcoming-appointments></upcoming-appointments>
  </div>
</template>
<script>
import GitHub from './git-hub';
import UpcomingAppointments from './upcoming-appointments';

const linksPerRow = 4;

export default {
  name: 'home-page',
  components: { GitHub, UpcomingAppointments },
  props: {
    config: Object,
  },
  mounted() {
    document.addEventListener('keydown', (event) => {
      const key = event.which;
      if (key === 37 || key === 38 || key === 39 || key === 40) {
        event.preventDefault();
      }
    });
  },
  data: function data() {
    return {
      linkSearch: '',
      currentFocus: 0,
    };
  },
  computed: {
    allLinks: function allLinks() {
      const links = [];
      this.config.fixed_links.forEach(({ url, icon, name, subs }) => {
        links.push({ url, name, icon });
        if (subs === undefined) return;
        subs.forEach(({ url: childUrl, name: childName }) => {
          links.push({ url: childUrl, icon, name: childName, parent: name });
        });
      });
      return links;
    },
    linkResults: function linkResults() {
      if (this.linkSearch === '') return this.config.fixed_links;
      return this.allLinks.filter((link) => {
        const lowerSearch = this.linkSearch.toLowerCase();
        const searchFields = [link.name.toLowerCase(), link.url.toLowerCase()];
        if (link.parent) searchFields.push(link.parent.toLowerCase());
        return searchFields.filter(field => field.includes(lowerSearch)).length > 0;
      });
    },
  },
  methods: {
    resetFocus() {
      this.currentFocus = 0;
    },
    goToFirstLink() {
      location.assign(this.linkResults[this.currentFocus].url);
    },
    setFocus() {
      const ref = this.$refs[this.linkResults[this.currentFocus].url][0];
      if (ref !== undefined) {
        this.$refs[this.linkResults[this.currentFocus].url][0].focus();
      }
    },
    setSearchFocus() {
      this.$refs.search.focus();
    },
    moveFocusRight() {
      this.currentFocus += 1;
      if (this.currentFocus >= this.linkResults.length) this.currentFocus = 0;
      this.setFocus(this.currentFocus);
    },
    moveFocusLeft() {
      this.currentFocus -= 1;
      if (this.currentFocus < 0) this.currentFocus = this.linkResults.length - 1;
      this.setFocus(this.currentFocus);
    },
    moveFocusUp() {
      const prevFocus = this.currentFocus;
      const maxIndex = this.linkResults.length - 1;

      this.currentFocus -= linksPerRow;
      if (this.currentFocus < 0) {
        if (this.linkResults.length <= linksPerRow) {
          this.currentFocus = prevFocus - 1 < 0 ? maxIndex : prevFocus - 1;
        } else {
          // Go to same column on bottom row
          let itemsInLastRow = this.linkResults.length % linksPerRow;
          if (itemsInLastRow === 0) itemsInLastRow = linksPerRow;
          this.currentFocus = (this.linkResults.length - itemsInLastRow) + prevFocus;
          if (this.currentFocus > maxIndex) {
            this.currentFocus -= linksPerRow;
          }
        }
      }
      this.setFocus(this.currentFocus);
    },
    moveFocusDown() {
      const prevFocus = this.currentFocus;
      const maxIndex = this.linkResults.length - 1;
      this.currentFocus += linksPerRow;
      if (this.currentFocus > maxIndex) {
        if (this.linkResults.length <= linksPerRow) {
          this.currentFocus = prevFocus + 1 > maxIndex ? 0 : prevFocus + 1;
        } else {
          // Go to same column on top row
          this.currentFocus = prevFocus % linksPerRow;
        }
      }
      this.setFocus(this.currentFocus);
    },
  },
};
</script>

<style lang="scss" scoped>
  @import "../styles/global.scss";

  .header {
    @include shadow;
    &__links {
      position: absolute;
      right: 16px;
      top:16px;
      @include breakpoint(xs) {
          display: none;
      }
    }
    &__title {
      padding: 6rem 2rem 2rem;
      font-size: 3rem;
    }
    &__quote {
      padding: 1rem;
      font-size: 1.2rem;
    }
  }

  .link {
    width: 80%;
    margin: 0 auto;

    &__search {
      font-size: 2rem;
      width: 100%;
      padding: 0 8px;
      border-radius: 8px;
    }
    &__results {
      width: 100%;
      margin: 0 auto;
      border-radius: 1rem;
      display: flex;
      flex-wrap: wrap;
      align-items: stretch;
      justify-content: center;
    }
    &__result {
      display: block;
      flex-basis: 25%;
    }
    &__link {
      display: block;
      background-color: $bg-color;
      margin: 1rem;
      padding: 1rem;
      border-radius: 16px;
      vertical-align: middle;
      transform: perspective(1px) translateZ(0);
      box-shadow: 0 0 1px transparent;
      color: $fg-color-light-purple;
      font-weight: 800;
      font-size: 1rem;
      font-family: $barlow-font;
      font-variant: small-caps;
      text-align: center;
      letter-spacing: 2px;
      text-underline-position: under;
      &:focus {

      }
      &:hover, &:focus, &:active {
       animation-duration: 1s;
       animation-name: wobble;
       animation-iteration-count: 1;
       animation-timing-function: ease-in-out;
      }
    }
    &__parent {
        color: $fg-color-blue;
    }
  }
</style>
