# Multistage Dockerfile

Python docker image tend to become large after installing the application requirements
(the slim base is ~150 MB uncompressed), therefore it's important to spend efforts
to minimise the image size, even if it produces a slightly more complex multistage
Dockerfile.

The implemented Dockerfile makes sure the production image will keep to a minimal size ("only" 360MB):
 * 150MB base image
 * 210MB python installed dependencies

If you look at the "dev" image is instead ~850MB, more than 400MB that would
end up as a cost in traffic on each image pull.

```mermaid
flowchart TD
    subgraph BASE
      base["Base
      ====
      Contains system runtime
      libraries necessary to run
      all the applications
      (e.g. libmysql)"]
  
      base_app["Base app
      ========
      Copies shared application logic
      independent from the used framework
      (domains, storage, etc.)"]
  
      base_builder["Base Builder
      ============
      Contains system libraries
      necessary to build python
      dependencies
      (e.g. gcc, library headers)"]

    end
    
    dev["Dev
    ===
    Fat image containing everything
    for local development"]

    base-->base_app
    base-->base_builder
    base----->dev
    
    subgraph HTTP
      http_builder["HTTP builder
          ============
          Installs requirements for
          HTTP app in a virtualenv"]
      http_app["HTTP app
        ========
        Copies HTTP app,
        shared logic
        and requirements
        from previous containers"]
      http_builder-->http_app
    end
    
    subgraph Dramatiq
      dramatiq_builder["Dramatiq builder
          ============
          Installs requirements for
          Dramatiq worker in a virtualenv"]
      dramatiq_app["HTTP app
        ========
        Copies Dramatiq worker app,
        shared logic
        and requirements
        from previous containers"]
      dramatiq_builder-->dramatiq_app
    end
    
    base_builder-->http_builder
    base_builder-->dramatiq_builder
    base_app-->http_app
    base_app-->dramatiq_app
```
