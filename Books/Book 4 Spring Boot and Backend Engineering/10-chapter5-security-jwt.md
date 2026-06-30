# Chapter 5: Security — JWT Authentication

## 5.1 Why stateless authentication

Traditional server-side sessions store a session object (usually the authenticated user's identity) in server memory (or a shared database/cache like Redis), keyed by a session ID that the client holds in a cookie. Every request the client makes, the server looks up that session ID, finds the matching in-memory object, and knows who's asking.

Stateless authentication stores nothing on the server. The client holds *all* the state needed to prove identity — a signed token containing the user's identity and claims — and sends it with every request. The server validates the token's signature and reads the claims directly from the token, with no shared storage involved.

The advantages for a horizontally-scaled API like ours are concrete:

**Any instance can authenticate any request.** With server-side sessions and multiple instances of the same application running behind a load balancer, a request from user Alice that hits Instance A creates a session *on Instance A*. If the next request from Alice is routed to Instance B (which it might be, because load balancers typically don't guarantee "sticky" routing), Instance B has no session for Alice and treats her as unauthenticated. The fix is "sticky sessions" (the load balancer always routes Alice to Instance A) — which eliminates the load-balancing benefit — or a shared session store (Redis, database) — which makes the session store a shared dependency and a potential bottleneck. Stateless JWT validation requires no coordination between instances at all; every instance validates the signature independently.

**No session store to maintain.** One less infrastructure component, one less failure mode, one less thing to scale.

The trade-off: with stateless tokens, revocation is hard. A valid JWT is valid until it expires. If you need to invalidate a token before it expires (user logs out, user is banned, token is compromised), you need a server-side token blocklist — which partially reintroduces the statefulness you were trying to avoid. A common mitigation is short expiration times (15–60 minutes) with a longer-lived refresh token used to get a new access token silently, so the blast radius of a compromised token is bounded in time even if revocation is imperfect.

## 5.2 JWT structure

A JWT (JSON Web Token) is three Base64URL-encoded JSON segments joined by dots: `header.payload.signature`.

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
`alg` names the signing algorithm — `HS256` is HMAC-SHA256, a symmetric algorithm (the same secret key signs and verifies, so only your own servers can verify). For distributed systems where the verifier is a different service than the signer, `RS256` (RSA SHA-256, asymmetric) is common — the private key signs, the public key verifies, and the public key can be distributed freely without compromising the secret.

**Payload:**
```json
{
  "sub": "42",
  "email": "alice@example.com",
  "role": "CUSTOMER",
  "iat": 1718700000,
  "exp": 1718703600
}
```
The fields `sub` (subject — the user identifier), `iat` (issued-at timestamp), and `exp` (expiration timestamp, in Unix epoch seconds) are standard registered claims. Everything else (`email`, `role`) is custom. `exp` is what the server checks on every request to determine whether the token has expired.

**Signature:**
```
HMAC-SHA256(
  Base64URL(header) + "." + Base64URL(payload),
  secret_key
)
```
The signature covers both the header and payload, which means you can verify the entire token contents haven't been tampered with — any modification to the payload (like changing `"role": "CUSTOMER"` to `"role": "ADMIN"`) changes the bytes that the signature covers and makes the verification fail. The signature does *not* encrypt the payload — Base64URL encoding is trivially reversible; anyone who obtains the token can read its contents. Never put secrets in a JWT payload.

## 5.3 Adding the dependency

```xml
<!-- jjwt (Java JWT library) — add to pom.xml -->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.12.6</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.12.6</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.12.6</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

## 5.4 Configuration properties

```yaml
# application.yml (accumulated — add this section)
ordermanagement:
  security:
    jwt-secret: "5f4dcc3b5aa765d61d8327deb882cf99a2b7f3a6e8c0d5b4f9e1234567890ab"
    jwt-expiration-ms: 3600000       # 1 hour
    jwt-refresh-expiration-ms: 604800000  # 7 days
```

In production, `jwt-secret` comes from an environment variable (`ORDERMANAGEMENT_SECURITY_JWT_SECRET`), never committed to source control. A 256-bit (32 byte = 64 hex chars) random secret is the minimum for HS256.

```java
package com.example.ordermanagement.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ordermanagement.security")
public record SecurityProperties(
        String jwtSecret,
        long jwtExpirationMs,
        long jwtRefreshExpirationMs
) {}
```

## 5.5 `JwtService`

```java
package com.example.ordermanagement.security;

import com.example.ordermanagement.config.SecurityProperties;
import com.example.ordermanagement.entity.User;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class JwtService {

    private final SecurityProperties securityProperties;

    private SecretKey signingKey() {
        byte[] keyBytes = securityProperties.jwtSecret()
                .getBytes(StandardCharsets.UTF_8);
        return Keys.hmacShaKeyFor(keyBytes);
    }

    public String generateToken(User user) {
        return generateToken(Map.of(), user, securityProperties.jwtExpirationMs());
    }

    public String generateRefreshToken(User user) {
        return generateToken(Map.of("type", "refresh"), user,
                securityProperties.jwtRefreshExpirationMs());
    }

    private String generateToken(Map<String, Object> extraClaims, User user, long expirationMs) {
        return Jwts.builder()
                .claims(extraClaims)
                .subject(user.getId().toString())
                .claim("email", user.getEmail())
                .claim("role", user.getRole().name())
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + expirationMs))
                .signWith(signingKey())
                .compact();
    }

    public Long extractUserId(String token) {
        return Long.parseLong(extractClaims(token).getSubject());
    }

    public String extractEmail(String token) {
        return extractClaims(token).get("email", String.class);
    }

    public boolean isTokenValid(String token) {
        try {
            Claims claims = extractClaims(token);
            return claims.getExpiration().after(new Date());
        } catch (JwtException | IllegalArgumentException e) {
            log.debug("Invalid JWT token: {}", e.getMessage());
            return false;
        }
    }

    private Claims extractClaims(String token) {
        return Jwts.parser()
                .verifyWith(signingKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }
}
```

## 5.6 Making `User` a Spring Security `UserDetails`

Spring Security's `UserDetails` is the interface that represents an authenticated principal. By implementing it directly on our `User` entity, we avoid a separate adapter class and can use `@AuthenticationPrincipal User currentUser` directly in controllers:

```java
// Add to User.java — replace the earlier version entirely:

package com.example.ordermanagement.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.time.Instant;
import java.util.Collection;
import java.util.List;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
public class User implements UserDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String username;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    @Column(nullable = false)
    private String password;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private Role role;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    public User(String username, String email, String password, Role role) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.role = role;
    }

    // UserDetails interface — Spring Security uses these:
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        // "ROLE_" prefix is Spring Security's convention — @PreAuthorize("hasRole('ADMIN')")
        // automatically prepends it, so we need it here to match.
        return List.of(new SimpleGrantedAuthority("ROLE_" + role.name()));
    }

    @Override
    public boolean isAccountNonExpired() { return true; }

    @Override
    public boolean isAccountNonLocked() { return true; }

    @Override
    public boolean isCredentialsNonExpired() { return true; }

    @Override
    public boolean isEnabled() { return true; }
}
```

```java
package com.example.ordermanagement.service;

import com.example.ordermanagement.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    @Override
    @Transactional(readOnly = true)
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        return userRepository.findByEmail(email)
                .orElseThrow(() -> new UsernameNotFoundException(
                        "User not found with email: " + email));
    }
}
```

## 5.7 `JwtAuthenticationFilter`

`OncePerRequestFilter` guarantees this filter runs exactly once per HTTP request — some filter chains can call a filter multiple times for a single request (e.g., during a forward or include); `OncePerRequestFilter` prevents that:

```java
package com.example.ordermanagement.security;

import com.example.ordermanagement.service.CustomUserDetailsService;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.lang.NonNull;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
@RequiredArgsConstructor
@Slf4j
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final CustomUserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain) throws ServletException, IOException {

        final String authHeader = request.getHeader("Authorization");

        // No token present — pass through unchanged. SecurityFilterChain will
        // reject the request later if the endpoint requires authentication.
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        final String jwt = authHeader.substring(7); // strip "Bearer "

        try {
            if (!jwtService.isTokenValid(jwt)) {
                filterChain.doFilter(request, response);
                return;
            }

            String email = jwtService.extractEmail(jwt);

            // Only populate the SecurityContext if it's not already set —
            // avoids redundant work if another filter already authenticated this request.
            if (email != null
                    && SecurityContextHolder.getContext().getAuthentication() == null) {

                UserDetails userDetails = userDetailsService.loadUserByUsername(email);

                UsernamePasswordAuthenticationToken authToken =
                        new UsernamePasswordAuthenticationToken(
                                userDetails,           // principal — what @AuthenticationPrincipal returns
                                null,                  // credentials — not needed post-authentication
                                userDetails.getAuthorities());

                authToken.setDetails(
                        new WebAuthenticationDetailsSource().buildDetails(request));

                SecurityContextHolder.getContext().setAuthentication(authToken);
                log.debug("Authenticated user '{}' for request {}", email, request.getRequestURI());
            }
        } catch (Exception e) {
            log.warn("JWT processing failed for {}: {}", request.getRequestURI(), e.getMessage());
        }

        filterChain.doFilter(request, response);
    }
}
```

The filter deliberately doesn't write an error response on failure — it just doesn't populate the `SecurityContext`. The `SecurityFilterChain` configured below will handle the missing authentication by returning `401 Unauthorized` for protected endpoints, while public endpoints proceed normally.

## 5.8 `AuthService` and `AuthController`

```java
package com.example.ordermanagement.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record RegisterRequest(
        @NotBlank String username,
        @NotBlank @Email String email,
        @NotBlank @Size(min = 8, message = "Password must be at least 8 characters") String password
) {}
```

```java
package com.example.ordermanagement.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public record LoginRequest(
        @NotBlank @Email String email,
        @NotBlank String password
) {}
```

```java
package com.example.ordermanagement.dto.response;

public record AuthResponse(String accessToken, String refreshToken, String tokenType) {
    public static AuthResponse of(String access, String refresh) {
        return new AuthResponse(access, refresh, "Bearer");
    }
}
```

```java
package com.example.ordermanagement.service;

import com.example.ordermanagement.dto.request.LoginRequest;
import com.example.ordermanagement.dto.request.RegisterRequest;
import com.example.ordermanagement.dto.response.AuthResponse;
import com.example.ordermanagement.entity.Role;
import com.example.ordermanagement.entity.User;
import com.example.ordermanagement.exception.DuplicateResourceException;
import com.example.ordermanagement.repository.UserRepository;
import com.example.ordermanagement.security.JwtService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;

    @Transactional
    public AuthResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new DuplicateResourceException(
                    "An account with email '" + request.email() + "' already exists");
        }
        if (userRepository.existsByUsername(request.username())) {
            throw new DuplicateResourceException(
                    "Username '" + request.username() + "' is already taken");
        }
        User user = new User(
                request.username(),
                request.email(),
                passwordEncoder.encode(request.password()),
                Role.CUSTOMER);
        userRepository.save(user);
        return AuthResponse.of(jwtService.generateToken(user),
                               jwtService.generateRefreshToken(user));
    }

    public AuthResponse login(LoginRequest request) {
        // AuthenticationManager validates credentials — throws AuthenticationException
        // (specifically BadCredentialsException) if username/password don't match.
        // Spring Security handles the password comparison against the BCrypt hash.
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.email(), request.password()));

        User user = userRepository.findByEmail(request.email())
                .orElseThrow(); // won't throw — authenticate() above would have already

        return AuthResponse.of(jwtService.generateToken(user),
                               jwtService.generateRefreshToken(user));
    }
}
```

```java
package com.example.ordermanagement.controller;

import com.example.ordermanagement.dto.request.LoginRequest;
import com.example.ordermanagement.dto.request.RegisterRequest;
import com.example.ordermanagement.dto.response.AuthResponse;
import com.example.ordermanagement.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/v1/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody RegisterRequest request) {
        return ResponseEntity.ok(authService.register(request));
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }
}
```

## 5.9 `SecurityFilterChain` — the central configuration

```java
package com.example.ordermanagement.config;

import com.example.ordermanagement.security.JwtAuthenticationFilter;
import com.example.ordermanagement.service.CustomUserDetailsService;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity       // enables @PreAuthorize on controller/service methods
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;
    private final CustomUserDetailsService userDetailsService;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            // CSRF: disabled for stateless JWT APIs.
            // CSRF protects against cross-site requests that *rely on the browser
            // automatically sending a session cookie*. JWT tokens must be explicitly
            // attached by JavaScript code, which cross-site requests can't do under
            // CORS policy. Re-enable if you ever add cookie-based sessions.
            .csrf(AbstractHttpConfigurer::disable)

            // CORS: delegate to the CorsConfigurationSource bean below.
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))

            // Session: STATELESS — no HttpSession is created or used.
            // Spring Security will not persist authentication state between requests.
            .sessionManagement(session ->
                    session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))

            // Authorization rules — evaluated top to bottom; first match wins.
            .authorizeHttpRequests(auth -> auth
                    // Public endpoints — no token required
                    .requestMatchers("/v1/auth/**").permitAll()
                    .requestMatchers(HttpMethod.GET, "/v1/products/**").permitAll()
                    .requestMatchers("/v1/health", "/actuator/**").permitAll()
                    .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
                    // Everything else requires a valid JWT
                    .anyRequest().authenticated()
            )

            // Insert our JWT filter before Spring's default username/password filter.
            // Our filter populates the SecurityContext; the rest of the chain uses it.
            .authenticationProvider(authenticationProvider())
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of(
                "http://localhost:3000",    // local React dev server
                "https://ordermanagement.com"
        ));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("Authorization", "Content-Type", "Idempotency-Key"));
        config.setExposedHeaders(List.of("Location"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L); // preflight cache duration in seconds

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }

    @Bean
    public AuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder());
        return provider;
    }

    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        // BCrypt with default strength (10 rounds) — strong enough for production,
        // fast enough to not noticeably slow login on modern hardware.
        return new BCryptPasswordEncoder();
    }
}
```

## 5.10 Method-level security: `@PreAuthorize`

With `@EnableMethodSecurity`, individual service or controller methods can be protected with SpEL expressions evaluated against the current authentication:

```java
// Only ADMIN users can call this — Spring Security checks before the method runs
@PreAuthorize("hasRole('ADMIN')")
public void deleteProduct(Long id) { ... }

// A user can access their own data, or an ADMIN can access anyone's
@PreAuthorize("#userId == authentication.principal.id or hasRole('ADMIN')")
public Page<OrderResponse> getOrdersForUser(Long userId, Pageable pageable) { ... }
```

`hasRole('ADMIN')` automatically matches against authorities prefixed with `ROLE_` — which is exactly what `User.getAuthorities()` returns (`"ROLE_ADMIN"`, `"ROLE_CUSTOMER"`). `authentication.principal` is the `UserDetails` object (our `User` entity) that the `JwtAuthenticationFilter` placed in the `SecurityContext`.

## 5.11 CORS and CSRF: why each is configured as it is

**CORS** (Cross-Origin Resource Sharing) is a browser security mechanism that blocks a web page from making requests to a different origin (scheme + domain + port) than the page was loaded from — unless the *server* explicitly tells the browser that cross-origin requests from that origin are allowed. It doesn't protect against curl, Postman, or server-to-server calls — only browser-initiated cross-origin requests. We configure it explicitly so that our React frontend (on `localhost:3000` in development, `ordermanagement.com` in production) can call our API (on `localhost:8080`/`api.ordermanagement.com`) without the browser blocking it.

**CSRF** (Cross-Site Request Forgery) protection exists specifically to protect against attacks where a malicious site tricks a user's browser into making an *authenticated request to your API* without the user's knowledge — using the session cookie that the browser automatically attaches to requests to your domain. Because our API uses JWT tokens (which must be *explicitly* attached to requests by JavaScript code, and cannot be read or sent by a different origin's JavaScript under CORS policy), the attack vector CSRF defends against doesn't apply. Disabling CSRF for a stateless JWT API isn't a security shortcut — it's the correct configuration for the threat model. If you add cookie-based authentication later, re-enable it.

> **Interview Question — SDE-2:** "Walk through what happens to an HTTP request from the moment it hits the server until `@AuthenticationPrincipal User currentUser` is populated in a controller method."
>
> **Answer:** The embedded Tomcat servlet container receives the request and passes it through Spring Security's `FilterChainProxy`, which applies the configured `SecurityFilterChain`. The filters run in order. `JwtAuthenticationFilter` (inserted before `UsernamePasswordAuthenticationFilter`) runs first: it reads the `Authorization` header, strips the `Bearer ` prefix, calls `JwtService.isTokenValid()` which parses and verifies the HMAC-SHA256 signature and checks the expiration claim, then calls `CustomUserDetailsService.loadUserByUsername()` with the email extracted from the token to load the full `User` entity from the database (yes, this is one database query per authenticated request — a common optimization is caching here, or embedding enough claims in the JWT to avoid the lookup entirely for simple role checks). It then constructs a `UsernamePasswordAuthenticationToken` with the loaded `UserDetails` as the principal and the user's granted authorities, and sets it on `SecurityContextHolder.getContext()`. The rest of the filter chain and eventually the `DispatcherServlet` can now see an authenticated `Authentication` object in the `SecurityContext`. When Spring MVC invokes the controller method and encounters `@AuthenticationPrincipal`, it resolves the argument by calling `SecurityContextHolder.getContext().getAuthentication().getPrincipal()` and casting it to the declared parameter type (`User`).

---

The API is now secure. Chapter 6 tests it — systematically, at every layer, with tools that actually catch the kinds of bugs tests at only one layer would miss.
