# OAuth Token Scope Resolution Guide

## 🎯 Objective

Fix GitHub OAuth token scope to enable pushing workflow files and complete LFS migration.

## 🔍 Current Issue

- **Problem**: OAuth token lacks `workflow` scope
- **Symptom**: Cannot push `.github/workflows/` files
- **Impact**: Blocks complete LFS migration push to GitHub

## 🛠️ Solution Options

### Option 1: Update Existing Token (Recommended)

1. **Open GitHub Settings**: <https://github.com/settings/tokens>
2. **Find your current token** in the list
3. **Click "Edit"** or the token name
4. **Scroll to "Select scopes"** section
5. **Check the "workflow" checkbox** ✅
6. **Click "Update token"** at the bottom
7. **Done!** Your existing token now has workflow scope

### Option 2: Create New Token

1. **Open New Token Page**: <https://github.com/settings/tokens/new>
2. **Name**: "Development Token with Workflow"
3. **Expiration**: Choose appropriate duration
4. **Select scopes**:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `write:packages` (Upload packages - optional)
5. **Generate token**
6. **⚠️ COPY IMMEDIATELY** - you won't see it again!

## 🧪 Testing After Update

### Test 1: Basic Push

```powershell
cd "C:\dev\Projects\openai-url-harvester"
git push origin HEAD
```

### Test 2: Workflow File Push

```powershell
# If you have workflow files to push
git add .github/workflows/
git commit -m "Add GitHub workflows"
git push origin HEAD
```

## 🚀 Next Steps After Token Update

1. **Test Push Capability**
   - Try pushing from any repository
   - Git will prompt for new credentials
   - Use your updated/new token as password

2. **Push All LFS Migrations**
   - All 11 projects ready to push
   - LFS files properly configured
   - Backup branches created for safety

3. **Verify LFS Storage**
   - Check GitHub repository sizes
   - Confirm LFS files show as "Stored with Git LFS"
   - Validate repository performance improvements

## 📊 Migration Status Summary

### ✅ Completed (Ready to Push)

- **Priority 1**: 9 projects (content-extractors + doc-harvesters)
- **Priority 2**: 2 projects (openai-url-harvester + html-to-markdown-v4)
- **Total**: ~860MB moved to LFS
- **Backup**: backup-pre-lfs-20251009 branches created

### 🔄 Pending OAuth Resolution

- Push all LFS changes to GitHub
- Sync workflow files to repositories
- Complete migration verification

## 🆘 Troubleshooting

### If Push Still Fails After Token Update

1. **Clear Git Credentials**:

   ```powershell
   git config --global --unset credential.helper
   git config --global credential.helper manager-core
   ```

2. **Force Credential Refresh**:

   ```powershell
   git push origin HEAD
   # When prompted, use NEW token as password
   ```

3. **Check Token Scopes**:
   - Verify `workflow` scope is checked ✅
   - Ensure token hasn't expired
   - Confirm token has correct repository access

### If You Need to Start Over

1. All changes are safely committed locally
2. Backup branches exist for rollback
3. Can regenerate token with correct scopes
4. LFS migration can be re-run if needed

## 📞 Ready to Continue?

After updating your token, return to the terminal and we'll:

1. Test the new token scope
2. Push all LFS migrations
3. Verify successful GitHub integration
4. Complete the migration process!

---
*Created: 2025-01-09*
*Status: Awaiting OAuth token scope update*
