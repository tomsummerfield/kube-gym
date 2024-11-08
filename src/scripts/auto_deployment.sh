#! /bin/bash

# Script to remove all the containers and images from the local docker registry
# and then build and run the containers again.
# This scripts will call kubectl to delete the existing deployment
# and then apply the new deployment.


