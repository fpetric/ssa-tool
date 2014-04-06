(local-set-key
 (kbd "C-c ,")
 (lambda (key)
   (interactive "sKey: ")
   (insert (format "#%% %s %%#\n#%% end-%s %%#" key key))))
