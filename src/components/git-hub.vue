<template>
<div v-if="isLoaded">
  <h2 class="gh__title"><span class="fab fa-github"></span> Scribe</h2>
  <div class="gh__container">
    <div v-for="(prType, index) in prTypes" :key="`prtype-${index}`" class="gh__type-container">
      <h3 class="gh__type-title">{{ prType[0] }}</h3>
      <h4 v-if="prType[1].length === 0">All Set Here!</h4>
      <div v-for="pr in prType[1]" :key="pr.url" class="gh__pr-container">
        <a class="gh__pr-title" :href="pr.html_url">{{ pr.title }}</a>
        <p class="gh__markdown" v-html="$options.filters.markdown(pr.body)"></p>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import Remarkable from 'remarkable';

const md = new Remarkable();

export default {
  name: 'git-hub',
  created() {
    const vthis = this;
    return axios.get('/start-api/v1/github')
      .then((response) => {
        response.data['review-requests'].forEach((pr) => { vthis.reviewRequests.push(pr); });
        response.data.approved.forEach((pr) => { vthis.approved.push(pr); });
        response.data['changes-requested'].forEach((pr) => { vthis.changesRequested.push(pr); });
        vthis.isLoaded = true;
      });
  },
  computed: {
    prTypes() {
      return [
        ['Review Requests', this.reviewRequests],
        ['Approved', this.approved],
        ['Changes Requested', this.changesRequested],
      ];
    },
  },
  data() {
    return {
      isLoaded: false,
      reviewRequests: [],
      approved: [],
      changesRequested: [],
    };
  },
  filters: {
    markdown(value) {
      return md.render(value);
    },
  },
};
</script>  

<style lang="scss">
@import "../styles/global.scss";
.gh {
    &__title {
        @include shadow;
        font-size: 3rem;
        margin-top: 2rem;
    }

    &__container {
        margin: 16px 0 0 0;
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
        color: $fg-color-primary;
        // Permalink - use to edit and share this gradient:
        // http://colorzilla.com/gradient-editor/#483c4b+0,1a161b+100&0.9+0,0.9+100
        background: -moz-radial-gradient(center, ellipse cover, rgba(72,60,75,0.9) 0%, rgba(26,22,27,0.9) 70%);
        background: -webkit-radial-gradient(center, ellipse cover, rgba(72,60,75,0.9) 0%,rgba(26,22,27,0.9) 70%);
        background: radial-gradient(ellipse at center, rgba(72,60,75,0.9) 0%, rgba(26,22,27,0.9) 70%);
    }

    &__type-container {
        @include breakpoint(xs) {
            width: calc(100% - 4rem);
            max-width: calc(100% - 4rem);
        }
        padding: 2rem;
        max-width: calc(33% - 4rem);
        width: calc(33% - 4rem);
    }

    &__type-title {
        font-size: 1.8rem;
        color: $fg-color-light-purple;
        padding: 1rem 0;
    }

    &__pr-title {
        display: inline-block;
        font-size: 1.8rem;
        font-weight: bold;
        text-decoration: underline;
        color: #79b2a8;
        margin: 1rem 0;
    }

    &__pr-title:visited, &__pr-title:active {
        color: #79b2a8;
    }

    &__pr-title:hover {
	    color: #1a8976;
    }
    &__markdown {
        img {
            width: auto;
            height: auto;
            max-width: 100%;
            max-height: 100%;
        }
    }
}
  
</style>
