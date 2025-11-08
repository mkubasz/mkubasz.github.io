import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.date(),
    excerpt: z.string().optional(),
    categories: z.array(z.string()).optional(),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = { blog };
