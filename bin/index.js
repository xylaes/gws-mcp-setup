#!/usr/bin/env node

import { Command } from 'commander';
import Parser from 'rss-parser';
import chalk from 'chalk';
import inquirer from 'inquirer';
import open from 'open';

const parser = new Parser();

// Configure CLI commands/options
const program = new Command();
program
  .name('gnews')
  .description('A beautiful Node CLI tool to fetch and read Google News')
  .version('1.0.0')
  .option('-s, --search <query>', 'Search for specific news articles')
  .option('-t, --topic <topic>', 'Filter news by topic (business, technology, sports, science, health, world, nation)')
  .option('-l, --limit <number>', 'Limit the number of articles shown', (val) => parseInt(val, 10), 10)
  .option('-i, --interactive', 'Enable interactive mode to select and open articles')
  .parse(process.argv);

const options = program.opts();

// Predefined topic validation
const TOPICS = ['business', 'technology', 'sports', 'science', 'health', 'world', 'nation'];

function getFeedUrl(opts) {
  const baseUrl = 'https://news.google.com/rss';
  const params = 'hl=en-US&gl=US&ceid=US:en';

  if (opts.search) {
    return `${baseUrl}/search?q=${encodeURIComponent(opts.search)}&${params}`;
  }

  if (opts.topic) {
    const topicLower = opts.topic.toLowerCase();
    if (!TOPICS.includes(topicLower)) {
      console.warn(chalk.yellow(`Warning: "${opts.topic}" is not a recognized default topic.`));
      console.warn(chalk.yellow(`Available topics: ${TOPICS.join(', ')}`));
      console.warn(chalk.yellow('Attempting to fetch anyway...\n'));
    }
    return `${baseUrl}/headlines/section/topic/${topicLower.toUpperCase()}?${params}`;
  }

  return `${baseUrl}?${params}`;
}

function getRelativeTime(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  if (isNaN(diffMs)) return dateString;

  const diffMins = Math.floor(diffMs / 60000);
  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;

  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours}h ago`;

  const diffDays = Math.floor(diffHours / 24);
  return `${diffDays}d ago`;
}

function parseTitle(rawTitle) {
  const parts = rawTitle.split(' - ');
  if (parts.length > 1) {
    const source = parts.pop();
    const title = parts.join(' - ');
    return { title, source };
  }
  return { title: rawTitle, source: 'Google News' };
}

async function main() {
  const url = getFeedUrl(options);

  if (options.search) {
    console.log(chalk.cyan(`🔍 Searching Google News for: "${options.search}"...\n`));
  } else if (options.topic) {
    console.log(chalk.cyan(`📰 Fetching topic: ${options.topic.toLowerCase()}...\n`));
  } else {
    console.log(chalk.cyan('🌎 Fetching top stories...\n'));
  }

  try {
    const feed = await parser.parseURL(url);
    const items = feed.items.slice(0, options.limit);

    if (items.length === 0) {
      console.log(chalk.yellow('No articles found.'));
      return;
    }

    if (options.interactive) {
      const choices = items.map((item, index) => {
        const { title, source } = parseTitle(item.title);
        const timeStr = getRelativeTime(item.pubDate);
        return {
          name: `${chalk.blue(`${index + 1}.`)} ${title} ${chalk.green(`[${source}]`)} ${chalk.dim(`(${timeStr})`)}`,
          value: item.link
        };
      });

      choices.push(new inquirer.Separator());
      choices.push({ name: chalk.red('❌ Exit'), value: 'exit' });

      const answers = await inquirer.prompt([
        {
          type: 'list',
          name: 'articleUrl',
          message: 'Select an article to open in your browser:',
          choices: choices,
          pageSize: 15
        }
      ]);

      if (answers.articleUrl && answers.articleUrl !== 'exit') {
        try {
          const parsedUrl = new URL(answers.articleUrl);
          if (parsedUrl.protocol === 'http:' || parsedUrl.protocol === 'https:') {
            console.log(chalk.green(`\nOpening article in your default browser...`));
            await open(answers.articleUrl);
          } else {
            console.error(chalk.red('\nError: Only http and https URLs are allowed.'));
          }
        } catch (err) {
          console.error(chalk.red('\nError: Invalid URL.'));
        }
      }
    } else {
      // Print beautifully to terminal
      items.forEach((item, index) => {
        const { title, source } = parseTitle(item.title);
        const timeStr = getRelativeTime(item.pubDate);
        
        console.log(`${chalk.blue.bold(`${index + 1}.`)} ${chalk.white.bold(title)}`);
        console.log(`   Source: ${chalk.green(source)} | Published: ${chalk.dim(timeStr)}`);
        console.log(`   Link:   ${chalk.gray.underline(item.link)}`);
        console.log();
      });
    }
  } catch (error) {
    console.error(chalk.red('\nError fetching news from Google:'));
    console.error(chalk.red(error.message));
  }
}

main();
