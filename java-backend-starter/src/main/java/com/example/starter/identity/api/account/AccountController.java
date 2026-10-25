package com.example.starter.identity.api.account;

import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import com.example.starter.identity.application.CurrentUserService;
import com.example.starter.identity.domain.User;

@RestController
@RequestMapping("/api/v1/account")
public class AccountController {

    private final CurrentUserService currentUserService;

    public AccountController(CurrentUserService currentUserService) {
        this.currentUserService = currentUserService;
    }

    @GetMapping("/me")
    public MeResponse me(@AuthenticationPrincipal Jwt jwt) {
        User user = currentUserService.getCurrentUser(jwt);
        return MeResponse.from(user);
    }
}
