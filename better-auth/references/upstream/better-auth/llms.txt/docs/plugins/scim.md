# System for Cross-domain Identity Management (SCIM)

Integrate SCIM with your application.



System for Cross-domain Identity Management ([SCIM](https://simplecloud.info/#Specification)) makes managing identities in multi-domain scenarios easier to support via a standardized protocol.
This plugin exposes a [SCIM](https://simplecloud.info/#Specification) server that allows third party identity providers to sync identities to your service.

## Installation

<Steps>
  <Step>
    ### Install the plugin

    ```bash
    npm install @better-auth/scim
    ```
  </Step>

  <Step>
    ### Add Plugin to the server

    ```ts title="auth.ts"
    import { betterAuth } from "better-auth"
    import { scim } from "@better-auth/scim"; // [!code highlight]

    const auth = betterAuth({
        plugins: [ // [!code highlight]
            scim() // [!code highlight]
        ] // [!code highlight]
    })
    ```
  </Step>

  <Step>
    ### Enable HTTP methods

    SCIM requires the `POST`, `PUT`, `PATCH` and `DELETE` HTTP methods to be supported by your server.
    For most frameworks, this will work out of the box, but some frameworks may require additional configuration:

    <Tabs items={["Next.js", "Solid Start"]}>
      <Tab value="Next.js">
        ```ts title="api/auth/[...all]/route.ts"
        import { auth } from "@/lib/auth";
        import { toNextJsHandler } from "better-auth/next-js";

        export const { POST, GET, PUT, PATCH, DELETE } = toNextJsHandler(auth); // [!code highlight]
        ```
      </Tab>

      <Tab value="Solid Start">
        ```ts title="routes/api/auth/*auth.ts"
        import { auth } from "~/lib/auth";
        import { toSolidStartHandler } from "better-auth/solid-start";

        export const { GET, POST, PUT, PATCH, DELETE } = toSolidStartHandler(auth); // [!code highlight]
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step>
    ### Migrate the database

    Run the migration or generate the schema to add the necessary fields and tables to the database.

    <Tabs items={["migrate", "generate"]}>
      <Tab value="migrate">
        <CodeBlockTabs defaultValue="npm" groupId="persist-install" persist>
          <CodeBlockTabsList>
            <CodeBlockTabsTrigger value="npm">
              npm
            </CodeBlockTabsTrigger>

            <CodeBlockTabsTrigger value="pnpm">
              pnpm
            </CodeBlockTabsTrigger>

            <CodeBlockTabsTrigger value="yarn">
              yarn
            </CodeBlockTabsTrigger>

            <CodeBlockTabsTrigger value="bun">
              bun
            </CodeBlockTabsTrigger>
          </CodeBlockTabsList>

          <CodeBlockTab value="npm">
            ```bash
            npx @better-auth/cli migrate
            ```
          </CodeBlockTab>

          <CodeBlockTab value="pnpm">
            ```bash
            pnpm dlx @better-auth/cli migrate
            ```
          </CodeBlockTab>

          <CodeBlockTab value="yarn">
            ```bash
            yarn dlx @better-auth/cli migrate
            ```
          </CodeBlockTab>

          <CodeBlockTab value="bun">
            ```bash
            bun x @better-auth/cli migrate
            ```
          </CodeBlockTab>
        </CodeBlockTabs>
      </Tab>

      <Tab value="generate">
        <CodeBlockTabs defaultValue="npm" groupId="persist-install" persist>
          <CodeBlockTabsList>
            <CodeBlockTabsTrigger value="npm">
              npm
            </CodeBlockTabsTrigger>

            <CodeBlockTabsTrigger value="pnpm">
              pnpm
            </CodeBlockTabsTrigger>

            <CodeBlockTabsTrigger value="yarn">
              yarn
            </CodeBlockTabsTrigger>

            <CodeBlockTabsTrigger value="bun">
              bun
            </CodeBlockTabsTrigger>
          </CodeBlockTabsList>

          <CodeBlockTab value="npm">
            ```bash
            npx @better-auth/cli generate
            ```
          </CodeBlockTab>

          <CodeBlockTab value="pnpm">
            ```bash
            pnpm dlx @better-auth/cli generate
            ```
          </CodeBlockTab>

          <CodeBlockTab value="yarn">
            ```bash
            yarn dlx @better-auth/cli generate
            ```
          </CodeBlockTab>

          <CodeBlockTab value="bun">
            ```bash
            bun x @better-auth/cli generate
            ```
          </CodeBlockTab>
        </CodeBlockTabs>
      </Tab>
    </Tabs>

    See the [Schema](#schema) section to add the fields manually.
  </Step>
</Steps>

## Usage

Upon registration, this plugin will expose compliant [SCIM 2.0](https://simplecloud.info/#Specification) server. Generally, this server is meant to be consumed by a third-party (your identity provider), and will require a:

* **SCIM base URL**: This should be the fully qualified URL to the SCIM server (e.g `http://your-app.com/api/auth/scim/v2`)
* **SCIM bearer token**: See [generating a SCIM token](#generating-a-scim-token)

### Generating a SCIM token

Before your identity provider can start syncing information to your SCIM server,
you need to generate a SCIM token that your identity provider will use to authenticate against it.

A SCIM token is a simple bearer token that you can generate:


### Client Side

```ts
const { data, error } = await authClient.scim.generateToken({
    providerId: acme-corp,
    organizationId: the-org, // optional
});
```

### Server Side

```ts
const data = await auth.api.generateSCIMToken({
    body: {
        providerId: acme-corp,
        organizationId: the-org, // optional
    },
    // This endpoint requires session cookies.
    headers: await headers()
});
```

### Type Definition

```ts
type generateSCIMToken = {
    /**
    * The provider id
    */
    providerId: string = "acme-corp"
    /**
     * Optional organization id. When specified, the organizations plugin must also be enabled
    */
    organizationId?: string = "the-org"
  
}
```


A `SCIM` token is always restricted to a provider, thus you are required to specify a `providerId`. This can be any provider your instance supports (e.g one of the built-in providers such as `credentials` or an external provider registered through an external plugin such as `@better-auth/sso`).
Additionally, when the `organization` plugin is registered, you can optionally restrict the token to an organization via the `organizationId`.

<Callout>
  **Important:** By default, any authenticated user with access to your better-auth instance will be able to generate a SCIM token. This can be an important security risk to your application, especially in multi-tenant scenarios.
  It is highly recommended that you implement [hooks](#hooks) to restrict this access to certain roles or users:
</Callout>

```ts
const userRoles = new Set(["admin"]);
const userAdminIds = new Set(["some-admin-user-id"]);

scim({
    beforeSCIMTokenGenerated: async ({ user, member, scimToken }) => {
        // IMPORTANT: Use this hook to restrict access to certain roles or users
        // At the very least access must be restricted to admin users (see example below)

        const userHasAdmin = member?.role && userRoles.has(member.role);
        const userIsAdmin = userAdminIds.size > 0 && userAdminIds.has(user.id);

        if (!userHasAdmin && !userIsAdmin) {
            throw new APIError("FORBIDDEN", { message: "User does not have enough permissions" });
        }
    },
})
```

See the [hooks](#hooks) documentation for more details about supported hooks.

#### Default SCIM token

We also provide a way for you to specify a `SCIM` token to use by default. This allows you to test a SCIM connection without setting up providers in the database:

```ts title="auth.ts"
const auth = betterAuth({
    plugins: [
        scim({
            defaultSCIM: [
                {
                    providerId: "default-scim", // ID of the existing provider you want to provision
                    scimToken: "some-scim-token", // SCIM plain token
                    organizationId: "the-org" // Optional organization id
                }
            ]
        })
    ]
});
```

<Callout type="info">
  **Important**: Please note that you must base64 encode your `scimToken` before you try to use as follows: `base64(scimToken:providerId[:organizationId])`.

  In our example above, you would need to encode the `some-scim-token:default-scim:the-org` text to base64, resulting in the following scimToken: `c29tZS1zY2ltLXRva2VuOmRlZmF1bHQtc2NpbTp0aGUtb3Jn`
</Callout>

### SCIM endpoints

The following subset of the specification is currently supported:

#### List users

Get a list of available users in the database. This is restricted to list only users associated to the same provider and organization than your SCIM token.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.users({
    filter, // optional
});
```

### Server Side

```ts
const data = await auth.api.listSCIMUsers({
    query: {
        filter, // optional
    }
});
```

### Type Definition

```ts
type listSCIMUsers = {
      /**
       * SCIM compliant filter expression
      */
      filter?: string = 'userName eq "user-a"'
  
}
```


#### Get user

Get an user from the database. The user will be only returned if it belongs to the same provider and organization than the SCIM token.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.users.:userid({
    userId: user id,
});
```

### Server Side

```ts
const data = await auth.api.getSCIMUser({
    query: {
        userId: user id,
    }
});
```

### Type Definition

```ts
type getSCIMUser = {
      /**
       * Unique user identifier
      */
      userId: string = "user id"
  
}
```


#### Create new user

Provisions a new user to the database. The user will have an account associated to the same provider and will be member of the same org than the SCIM token.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.users({
    externalId: third party id, // optional
    name, // optional
    formatted: Daniel Perez, // optional
    givenName: Daniel, // optional
    familyName: Perez, // optional
});
```

### Server Side

```ts
const data = await auth.api.createSCIMUser({
    body: {
        externalId: third party id, // optional
        name, // optional
        formatted: Daniel Perez, // optional
        givenName: Daniel, // optional
        familyName: Perez, // optional
    }
});
```

### Type Definition

```ts
type createSCIMUser = {
      /*
       * Unique external (third party) identifier
      */
      externalId?: string = "third party id"
      /**
       * User name details
      */
      name?: {
          /**
           * Formatted name (takes priority over given and family name)
          */
          formatted?: string = "Daniel Perez"
          /**
           * Given name
          */
          givenName?: string = "Daniel"
          /**
           * Family name
          */
          familyName?: string = "Perez"
      
}
```


#### Update an existing user

Replaces an existing user details in the database. This operation can only update users that belong to the same provider and organization than the SCIM token.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.users.:userid({
    externalId: third party id, // optional
    name, // optional
    formatted: Daniel Perez, // optional
    givenName: Daniel, // optional
    familyName: Perez, // optional
});
```

### Server Side

```ts
const data = await auth.api.updateSCIMUser({
    query: {
        externalId: third party id, // optional
        name, // optional
        formatted: Daniel Perez, // optional
        givenName: Daniel, // optional
        familyName: Perez, // optional
    }
});
```

### Type Definition

```ts
type updateSCIMUser = {
      /*
       * Unique external (third party) identifier
      */
      externalId?: string = "third party id"
      /**
       * User name details
      */
      name?: {
          /**
           * Formatted name (takes priority over given and family name)
          */
          formatted?: string = "Daniel Perez"
          /**
           * Given name
          */
          givenName?: string = "Daniel"
          /**
           * Family name
          */
          familyName?: string = "Perez"
      
}
```


#### Partial update an existing user

Allows to apply a partial update to the user details. This operation can only update users that belong to the same provider and organization than the SCIM token.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.users.:userid({
    schemas,
    Operations,
});
```

### Server Side

```ts
const data = await auth.api.patchSCIMUser({
    query: {
        schemas,
        Operations,
    }
});
```

### Type Definition

```ts
type patchSCIMUser = {
      /**
       * Mandatory schema declaration
      */
      schemas: string[] = ["urn:ietf:params:scim:api:messages:2.0:PatchOp"]
      /**
       * List of JSON patch operations
      */
      Operations: Array<{ op: "replace" | "add" | "remove", path?: string, value: any 
}
```


#### Deletes a user resource

Completely deletes a user resource from the database. This operation can only delete users that belong to the same provider and organization than the SCIM token.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.users.:userid({
    userId,
});
```

### Server Side

```ts
const data = await auth.api.deleteSCIMUser({
    query: {
        userId,
    }
});
```

### Type Definition

```ts
type deleteSCIMUser = {
      userId: string
  
}
```


#### Get service provider config

Get SCIM metadata describing supported features of this server.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.serviceproviderconfig({});
```

### Server Side

```ts
const data = await auth.api.getSCIMServiceProviderConfig({});
```

### Type Definition

```ts
type getSCIMServiceProviderConfig = {
  
}
```


#### Get SCIM schemas

Get the list of supported SCIM schemas.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.schemas({});
```

### Server Side

```ts
const data = await auth.api.getSCIMSchemas({});
```

### Type Definition

```ts
type getSCIMSchemas = {
  
}
```


#### Get SCIM schema

Get the details of a supported SCIM schema.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.schemas.:schemaid({});
```

### Server Side

```ts
const data = await auth.api.getSCIMSchema({});
```

### Type Definition

```ts
type getSCIMSchema = {
  
}
```


#### Get SCIM resource types

Get the list of supported SCIM types.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.resourcetypes({});
```

### Server Side

```ts
const data = await auth.api.getSCIMResourceTypes({});
```

### Type Definition

```ts
type getSCIMResourceTypes = {
  
}
```


#### Get SCIM resource type

Get the details of a supported SCIM resource type.


### Client Side

```ts
const { data, error } = await authClient.scim.v2.resourcetypes.:resourcetypeid({});
```

### Server Side

```ts
const data = await auth.api.getSCIMResourceType({});
```

### Type Definition

```ts
type getSCIMResourceType = {
  
}
```


#### SCIM attribute mapping

By default, the SCIM provisioning will automatically map the following fields:

* `user.email`: User primary email or the first available email if there is not a primary one
* `user.name`: Derived from `name` (`name.formatted` or `name.givenName` + `name.familyName`) and fallbacks to the user primary email
* `account.providerId`: Provider associated to the `SCIM` token
* `account.accountId`: Defaults to `externalId` and fallbacks to `userName`
* `member.organizationId`: Organization associated to the provider

## Schema

The plugin requires additional fields in the `scimProvider` table to store the provider's configuration.

<DatabaseTable
  fields={[
      {
          name: "id", type: "string", description: "A database identifier", isRequired: true, isPrimaryKey: true,
      },
      { name: "providerId", type: "string", description: "The provider ID. Used to identify a provider and to generate a redirect URL.", isRequired: true, isUnique: true },
      { name: "scimToken", type: "string", description: "The SCIM bearer token. Used by your identity provider to authenticate against your server", isRequired: true, isUnique: true },
      { name: "organizationId", type: "string", description: "The organization Id. If provider is linked to an organization.", isRequired: false },
  ]}
/>

## Options

### Server

* `defaultSCIM`: Default list of SCIM tokens for testing.
* `storeSCIMToken`: The method to store the SCIM token in your database, whether `encrypted`, `hashed` or `plain` text. Default is `plain` text.

Alternatively, you can pass a custom encryptor or hasher to store the SCIM token in your database.

**Custom encryptor**

```ts title="auth.ts"
scim({
    storeSCIMToken: { 
        encrypt: async (scimToken) => {
            return myCustomEncryptor(scimToken);
        },
        decrypt: async (scimToken) => {
            return myCustomDecryptor(scimToken);
        },
    }
})
```

**Custom hasher**

```ts title="auth.ts"
scim({
    storeSCIMToken: {
        hash: async (scimToken) => {
            return myCustomHasher(scimToken);
        },
    }
})
```

### Hooks

The following hooks allow to intercept the lifecycle of the `SCIM` token generation:

```ts
scim({
    beforeSCIMTokenGenerated: async ({ user, member, scimToken }) => {
        // Callback called before the scim token is persisted
        // can be useful to intercept the generation
        if (member?.role !== "admin") {
            throw new APIError("FORBIDDEN", { message: "User does not have enough permissions" });
        }
    },
    afterSCIMTokenGenerated: async ({ user, member, scimToken, scimProvider }) => {
        // Callback called after the scim token has been persisted
        // can be useful to send a notification or otherwise share the token
        await shareSCIMTokenWithInterestedParty(scimToken);
    },
})
```

<Callout>
  **Note**: All hooks support error handling. Throwing an error in a before hook will prevent the operation from proceeding.
</Callout>

