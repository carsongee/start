<template>
  <div id="home-page">
    <div class="header">
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
        v-model="linkSearch"
        placeholder="Search Links"
        autofocus
        />
      <ul class="link__results">
        <li class="link__result" v-for="link in linkResults" :key="link.url">
          <a class="link__link" :href="link.url" target="_blank">
            <span class="link__parent" v-if="link.parent">{{ link.parent }} &gt; </span>
            {{ link.name }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'home-page',
    computed: {
      allLinks: function allLinks() {
        const links = [];
        this.config.fixed_links.forEach(({ url, name, subs }) => {
          links.push({ url, name });
          if (subs === undefined) return;
          subs.forEach(({ url: childUrl, name: childName }) => {
            links.push({ url: childUrl, name: childName, parent: name });
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
    data: function data() {
      return {
        linkSearch: '',
      };
    },
    props: {
      config: Object,
    },
  };
</script>

<style lang="scss" scoped>
  @keyframes wobble {
	16.65% { transform: skew(-12deg); }
	33.3% { transform: skew(10deg); }
	49.95% {transform: skew(-6deg);}
	66.6% { transform: skew(4deg); }
	83.25% { transform: skew(-2deg); }
	100% { transform: skew(0); }
  }
  
  .header {
    color: white;
    text-shadow:
    -2px -2px 1px #1e1e1e,
    2px -2px 1px #1e1e1e,
    -2px 2px 1px #1e1e1e,
    2px 2px 1px #1e1e1e;
    text-align: center;
    &__title {
      padding: 2rem;
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
      padding: 0 2rem;
      border-radius: 1rem;
    }
    &__results {
      width: 100%;
      margin: 0 auto;
      padding: 0 2rem;
      border-radius: 1rem;
      display: flex;
      flex-wrap: wrap;
      align-items: stretch;
      justify-content: center;
    }
    &__result {
      display: block;
      flex-basis: 20%;
    }
    &__link {
      display: block;
      background-color: rgba(26,22,27, .90);
      margin: 1rem;
      padding: 1rem;
      border-radius: 16px;
      vertical-align: middle;
      transform: perspective(1px) translateZ(0);
      box-shadow: 0 0 1px transparent;
      color: #a47ea5;
      font-weight: 800;
      font-size: 1rem;
      font-family: 'Barlow Semi Condensed', sans-serif;
      font-variant: small-caps;
      text-align: center;
      letter-spacing: 2px;
      text-underline-position: under;
      &:hover, &:focus, &:active {
	   animation-duration: 1s;
	   animation-name: wobble;
	   animation-iteration-count: 1;
	   animation-timing-function: ease-in-out;
      }
    }
    &__parent {
        color: #6f90b0;
    } 
  }
</style>
