#!/usr/bin/env bash
ssh your_username@your_server_address -p your_server_ssh_port "cd ~/projects/pmp/deploy && docker-compose up --build"
